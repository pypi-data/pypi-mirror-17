# qtMUD

[![codecov](https://codecov.io/gh/emsenn/qtmud/branch/master/graph/badge.svg)](https://codecov.io/gh/emsenn/qtmud)
[![Documentation Status](https://readthedocs.org/projects/qtmud/badge/?version=latest)](http://qtmud.readthedocs.io/en/latest/?badge=latest)
[![Requirements Status](https://requires.io/github/emsenn/qtmud/requirements.svg?branch=master)](https://requires.io/github/emsenn/qtmud/requirements/?branch=master)

qtMUD is a Python3 package for developing and hosting MUDs, Multi-User 
Dimensions.

Complete documentation is available locally at 
[ReadTheDocs](http://qtmud.readthedocs.io/en/latest/).

* [Purpose](Purpose)
* [Installation](#Installation)
* [Usage](#Usage)


## Installation

```bash
$ pip install qtmud
```

## Usage

The qtMUD package provides methods for running qtMUD as a socket server 
clients can connect to:

```python
>>> import qtmud
>>> qtmud.load()
qtmud        INFO     qtmud.load() called
qtmud        INFO     adding qtmud.subscriptions to qtmud.subscribers
qtmud        INFO     adding qtmud.services to qtmud.active_services
qtmud        INFO     qtmud.load()ed
True
>>> qtmud.start()
qtmud        INFO     start()ing active_services
qtmud        INFO     start()ing MUDSocket
qtmud        INFO     MUDSocket successfully bound to ('localhost', 5787)
qtmud        INFO     MUDSocket successfully bound to ('localhost', 5788, 0, 0)
qtmud        INFO     mudsocket start()ed
qtmud        INFO     talker start()ed
True
>>> qtmud.run()
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
