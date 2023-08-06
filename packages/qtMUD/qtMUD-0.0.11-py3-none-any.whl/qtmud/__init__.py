""" The main qtmud module houses some constants, the Thing class, and methods
    for start()ing and tick()ing the MUD engine.
"""

#
import logging
import pickle
import types
import uuid
from inspect import getmembers, isfunction, isclass

from clint.textui import colored

from qtmud import cmds, services, subscriptions, txt

# GLOBAL REFERENCES
NAME = 'qtMUD'
""" Name of the MUD engine. """
__version__ = '0.0.11'
""" MUD engine version """
__url__ = 'https://qtmud.readthedocs.io/en/latest/'




IPv4_HOSTNAME = '0.0.0.0'
IPv4_MUDPORT = 5787
IPv6_HOSTNAME = 'localhost'
IPv6_MUDPORT = 5788
DATA_DIR = './data/'
LOG_DIR = './logs/'



MUDLIB = None

SPLASH = txt.SPLASH.format(**locals())
""" The text new connections see. """

client_accounts = dict()
""" Populated by load_client_accounts(), a list of client accounts stored by
registered name."""

events = dict()
""" Events scheduled to occur next tick, populated by :func:`schedule`."""
things = dict()
""" all the things that new_thing() has made"""
subscribers = dict()
""" Methods which will be called for any relevant :attr:`events`. Populated
by :func:`qtmud.load` to contain bound methods of the methods in
:mod:`qtmud.subscriptions` referenced by method name. """
active_services = dict()
""" Services which will have their tick() function called by
:func:`qtmud.tick`. Populated by :func:`qtmud.load` to contain instances of
the classes in :mod:`qtmud.services` referenced by class name. """
connected_clients = list()

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))
try:
    logging.basicConfig(filename=LOG_DIR+'debug.log', filemode='w',
                        format=('%(asctime)s %(name)-12s %(levelname)-8s '
                                '%(message)s'),
                        datefmt='%m-%d %H:%M',
                        level=logging.DEBUG)
except FileNotFoundError as err:
    print('%s so all logs will go to terminal', err)
log = logging.getLogger(NAME)
""" An instance of :class:`logging.Logger`, intended to be used as the main
logger for qtmud and the mudlib, called through `qtmud.logs`."""
log.addHandler(console)


def load():
    """ Most importantly, puts every function from
    :mod:`qtmud.subscriptions` and every class from :mod:`qtmud.services`
    into :attr:`subscribers` and :attr:`active_services`, respectively.

    After populating `subscribers` and `active_services`, calls the start()
    method for each class in `active_services`, then attempts to load
    :attr:`MUDLIB`, if one is specified, and finally calls
    :func:`load_client_accounts`.
    """
    global active_services
    global subscribers
    log.info('qtmud.load() called')
    log.info('adding qtmud.subscriptions to qtmud.subscribers')
    subscribers = {s[1].__name__: [s[1]] for
                   s in getmembers(subscriptions) if isfunction(s[1])}
    log.info('adding qtmud.services to qtmud.active_services')
    active_services = {t[1].__name__.lower(): t[1]() for
                       t in getmembers(services) if isclass(t[1])}
    if load_client_accounts():
        log.debug('qtmud.client_accounts populated from '
                  'qtmud.load_client_accounts()')
    log.info('qtmud.load()ed')
    log.debug('subscribers are: %s', ', '.join(subscribers))
    log.debug('active_services are: %s',
              ', '.join([s for s in active_services]))
    return True


def load_client_accounts(file=(DATA_DIR + 'qtmud_client_accounts.p')):
    """ Populates :attr:`qtmud.client_accounts` with the pickle file
    specified. """
    global client_accounts
    log.info('filling qtmud.client_accounts from %s', file)
    try:
        client_accounts = pickle.load(open(file, 'rb'))
        log.debug('qtmud.client_accounts filled from %s', file)
        return True
    except FileNotFoundError:
        log.debug('no save file found, making one at %s', file)
        save_client_accounts()
        return False


def new_client_account(name, password, birthtime=None):
    """ Create a new client account in :attr:`client_accounts`"""
    client_accounts[name.lower()] = {'name': name,
                                     'password': password}
    if birthtime:
        client_accounts[name]['birthtime'] = birthtime
    log.debug('made the new client %s', name)
    save_client_accounts()
    return client_accounts[name]

def embolden(text):
    for marker in ['**', '*', '``', '`']:
        text = text.split(marker)
        for word in text[1::2]:
            if word:
                text[text.index(word)] = '%^B_WHITE%^' + word + '%^'
        text = ''.join(text)
    return text


def pinkfish_parse(text, requester=None):
    colors = {'BLACK': colored.black,
              'RED': colored.red,
              'GREEN': colored.green,
              'YELLOW': colored.yellow,
              'BLUE': colored.blue,
              'MAGENTA': colored.magenta,
              'CYAN': colored.cyan,
              'WHITE': colored.white}
    debug = ''
    working_text = ''
    layers = []
    bold = False
    delimiter = '%^'
    split_text = [c for c in embolden(text).split(delimiter)]
    if len(split_text) <= 1:
        return text
    position = 0
    while position < len(split_text):
        chunk = split_text[position]
        if chunk in ['B_'+c for c in colors]:
            bold=True
            chunk = ''.join(chunk.split('_')[1:])
        if chunk in colors:
            layers.append((chunk, bold))
            position += 1
        elif layers:
            layer = layers[-1]
            working_text += colors[layer[0]](chunk, bold=layer[1])+'\033[0;0m'
            position += 1
            if position < len(split_text):
                if split_text[position] not in colors and \
                                split_text[position] not in ['B_' + c for c in
                                                             colors]:
                    layers.pop(-1)
        else:
            working_text += chunk
            position += 1
    return working_text+'\033[0;0m'


def run():
    """ main loop """
    log.info('qtmud.run()ning')
    try:
        while True:
            tick()
    except KeyboardInterrupt:
        log.info('shutdown started')
        schedule('shutdown')
        tick()


def save_client_accounts(file=(DATA_DIR + 'qtmud_client_accounts.p')):
    """ Saves a pickle of the current :attr:`client_accounts`."""
    log.debug('saving client_accounts to %s', file)
    try:
        pickle.dump(client_accounts, open(file, 'wb'))
        return True
    except FileNotFoundError as err:
        log.warning('failed to save client_accounts: %s', err)


def schedule(sub, **payload):
    """ Schedules a call to sub with payload passed as parameters.
    """
    if not subscribers.get(sub, []):
        log.warning('Tried to schedule a %s event, no subscribers '
                    'listen to it though.', sub)
        return False
    for method in subscribers.get(sub, []):
        if method not in events:
            events[method] = []
        events[method].append(payload)
    return True


def search_connected_clients_by_name(name):
    """ Searches through :attr:`connected_clients` for one with a matching
    name. *(Ignores case)*

        :param name:        The name of the client you're looking for.
        :return list:       A list of connected clients with that name.
                            (Should probably just have one element.)
    """
    return [connected_clients[connected_clients.index(c)] for c in
            connected_clients
            if hasattr(c, 'name') and c.name.lower() == name.lower()]


def search_client_accounts_by_name(name):
    """ Searches through the :attr:`client_accounts` for a client with a
    matching name. *(For convenience, ignores case)*

        :param name:        The name of the client you're looking for
        :return list:       A list of the clients with that name. (Should
                            probably just have one element.)
    """
    return [c for c in client_accounts.keys() if c.lower() == name.lower()]


def start():
    """ Calls the start() function in every service in
    :attr:`active_services`.
    """
    log.info('start()ing active_services')
    for service in active_services:
        log.info('%s start()ing', service)
        try:
            active_services[service].start()
            log.info('%s start()ed', service)
        except AttributeError:
            pass
        except RuntimeWarning as warning:
            log.warning('%s failed to start: %s', service, warning)
    return True


def tick():
    """ Processes the events in :attr:`current_events`, sending them out to
    the :attr:`subscribers` who are listening for them.

        Also calls tick() in every service in :attr:`active_services`
    """
    global events
    if events:
        current_events = events
        events = dict()
        for event in current_events:
            for call in current_events[event]:
                try:
                    event(**call)
                except Exception as err:
                    print(err)
    for service in active_services:
        try:
            active_services[service].tick()
        except AttributeError:
            pass
    return True


class Thing(object):
    """ Most objects clients interact with are Things

        Created with :func:`new_thing`, things are objects with a few
        attributes added on, mostly for enabling in-game reference of the
        objects.
    """

    def __init__(self, **kwargs):
        self._name = str()
        while True:
            self.identity = uuid.uuid4()
            if self.identity not in things.keys():
                break
        things[self.identity] = self
        """ Passed by :func:`new_thing`, `identity` is stored as a UUID """
        self.nouns = {'thing'}
        """ `nouns` represent lower-case nouns which may be used to reference
            the thing.
        """
        self.name = str(self.identity)
        self.adjectives = set()
        self.qualities = []
        self.update(kwargs)
        return

    @property
    def name(self):
        """ Properly-cased full name of a thing
            Any name a thing is given is also added to :attr:`Thing.nouns`,
            with the old name being removed. Same for adjectives.

            .. warning:: This has some wonkiness, in that "Eric Baez" can be
                         referred to as "Eric Baez" or "Baez" but not "Eric".
                         "Eric Thing" would work, though.
        """
        return self._name

    @name.setter
    def name(self, value):
        old_name = self._name.lower().split(' ')
        if len(old_name) > 1:
            old_adjectives = old_name[0:-1]
            for adjective in old_adjectives:
                try:
                    self.adjectives.remove(adjective)
                except KeyError:
                    pass
        try:
            self.nouns.remove(old_name[-1])
        except KeyError:
            pass
        new_name = value.lower().split(' ')
        self.nouns.add(new_name[-1])
        if len(new_name) > 1:
            adjectives = new_name[0:-1]
            for adjective in adjectives:
                self.adjectives.add(adjective)
        self.nouns.add(new_name[-1])
        self._name = value

    def update(self, attributes):
        """ Update multiple attributes of Thing at once.

            Example:
                >>> foo = Thing()
                >>> foo.update({'name': 'eric'})
                >>> foo.name
                eric

            .. warning:: Does not properly recognize setters
        """
        # todo account for custom setters
        for attribute, value in attributes.items():
            if hasattr(self, attribute):
                self.__dict__[attribute] = value
        return True


class Client(Thing):
    """ The thing which represents a client within qtmud.
    """

    def __init__(self, **kwargs):
        super(Client, self).__init__(**kwargs)
        self.addr = tuple()
        """ The client's address, represented by IP and port.
            .. warning:: Probably broken if you try and connect through IPv6
        """
        self.commands = {}
        """ A dict where keys will be the names of methods in :mod:`qtmud.cmds`
        and the value will be a pointer to that method.
        """
        for command, function in [m for m in getmembers(cmds) if
                                  isfunction(m[1])]:
            self.commands[command] = types.MethodType(function, self)
        self.input_parser = 'client_command_parser'
        """ The subscription which will be called when this client inputs a
        command. If you wish to overwrite the client's default command
        parser, you'll need to overwrite this."""
        self.send_buffer = str()
        """ The string representing data the client has received. Usually
        emptied each :func:`tick <qtmud.tick>` by
        :class:`MUDSocket <qtmud.services.MUDSocket>`"""
        self.recv_buffer = str()
        self.channels = list()
        """ All the :class:`Talker <qtmud.services.Talker>` channels the
        client is listening to. """