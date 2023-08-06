# CANDY Board service CLI

[![GitHub release](https://img.shields.io/github/release/CANDY-LINE/candy-board-cli.svg)](https://github.com/CANDY-LINE/candy-board-cli/releases/latest)
[![License BSD3](https://img.shields.io/github/license/CANDY-LINE/candy-board-cli.svg)](http://opensource.org/licenses/BSD-3-Clause)

A CLI tool to communicate with a CANDY Board service running on systemd

## pip Installation

```
$ pip install candy-board-cli
```

## pip Uninstallation

```
$ pip candy-board-cli
```

## Development

### Prerequisites

 * [pandoc](http://pandoc.org)
 * [pypandoc](https://pypi.python.org/pypi/pypandoc/1.2.0)

On Mac OS:

```
$ brew install pandoc
$ pip install pypandoc
```

### Local Installation test

```
$ ./setup.py install --record files.txt
```

### Local Uninstallation test

```
$ cat files.txt | xargs rm -rf
```

# Revision history
* 1.0.3
    - Make pypandoc dependency optional

* 1.0.2
    - Fix an issue where the code could exit after opening a socket which caused socket error on the socket server

* 1.0.1
    - Don't have users run modem reset command casually

* 1.0.0
    - Initial public release

* 0.0.1
    - Initial beta release


