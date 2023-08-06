# qtMUD

[![Join the chat at https://gitter.im/qtmud/Lobby](https://badges.gitter.im/qtmud/Lobby.svg)](https://gitter.im/qtmud/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![PyPI version](https://badge.fury.io/py/qtmud.svg)](https://badge.fury.io/py/qtmud)
[![Documentation Status](https://readthedocs.org/projects/qtmud/badge/?version=latest)](http://qtmud.readthedocs.io/en/latest/?badge=latest)

[![Code Climate](https://codeclimate.com/github/emsenn/qtmud/badges/gpa.svg)](https://codeclimate.com/github/emsenn/qtmud)
[![Build Status](https://travis-ci.org/emsenn/qtmud.svg?branch=master)](https://travis-ci.org/emsenn/qtmud)

[![Requirements Status](https://requires.io/github/emsenn/qtmud/requirements.svg?branch=master)](https://requires.io/github/emsenn/qtmud/requirements/?branch=master)

------

qtMUD is a Python3 package for developing and hosting MUDs, Multi-User 
Dimensions.

Complete documentation is available at 
[ReadTheDocs](http://qtmud.readthedocs.io/en/latest/).


## Usage

The qtMUD package comes with `./bin/qtmud_run`, which runs a socket server.


```bash
$ qtmud_run -h
usage: qtmud_run [-h] [-v | -q] [--conf CONF]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  show all logging messages
  -q, --quiet    show only warning & more severe messages
  --conf CONF    config file to use

$ qtmud_run
qtmud_run preparing to start qtmud 0.0.5
qtmud        INFO     qtmud.load() called
qtmud        INFO     adding qtmud.subscriptions to qtmud.subscribers
qtmud        INFO     adding qtmud.services to qtmud.active_services
qtmud        INFO     qtmud.load()ed
qtmud        INFO     filling qtmud.client_accounts from ./qtmud_client_accounts.p
qtmud        INFO     start()ing active_services
qtmud        INFO     talker start()ed
qtmud        INFO     start()ing MUDSocket
qtmud        INFO     MUDSocket successfully bound to ('0.0.0.0', 5787)
qtmud        INFO     MUDSocket successfully bound to ('localhost', 5788, 0, 0)
qtmud        INFO     mudsocket start()ed
qtmud        INFO     qtmud.run()ning
```
`KeyboardInterrupt` to end the `run()`ning process.

---

To connect as a client to the running socket server:

```bash
$ telnet localhost 5787
Trying ::1...
Connection failed: Connection refused
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.

qtmud               0.0.5

Successfully connected to qtmud, press enter to continue login...
```
While telnet is the easiest way to connect, we recommend the 
[tiny-fugue](https://github.com/kruton/tinyfugue) MUD client.