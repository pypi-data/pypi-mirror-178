<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/philip-pal2.svg?branch=main)](https://cirrus-ci.com/github/<USER>/philip-pal2)
[![ReadTheDocs](https://readthedocs.org/projects/philip-pal2/badge/?version=latest)](https://philip-pal2.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/philip-pal2/main.svg)](https://coveralls.io/r/<USER>/philip-pal2)
[![PyPI-Server](https://img.shields.io/pypi/v/philip-pal2.svg)](https://pypi.org/project/philip-pal2/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/philip-pal2.svg)](https://anaconda.org/conda-forge/philip-pal2)
[![Monthly Downloads](https://pepy.tech/badge/philip-pal2/month)](https://pepy.tech/project/philip-pal2)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/philip-pal2)
-->

[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)

# philip-pal2

The PHiLIP (Primitive Hardware In the Loop Integration Product) PAL (Protocol Abstraction Layer)

## Description

The application layer based on the `mm_pal` for `PHiLIP`.
Providing helpers and connection details specifically for PHiLIP.

### PHiLIP PAL Installation
As this is both a python library (Phil interface) and application (`philip-cli`) you may or may not want to install in a virtual environment.

Generally, a simple pip installation should work:
```
pip install philip-pal2
```

### Logging on to PHiLIP CLI
First connect PHiLIP to the computer so a serial port connection is available.

To log into PHiLIP run:
```
philip-cli
```

### Running single PHiLIP commands

Besides the full PHiLIP PAL Shell there is also CLI mode for simple one-shot
access to PHiLIP interface functions. It allows to reset the PHiLIP MCU and
the connected DUT.

After connecting PHiLIP simply run `python3 -m philip_pal --help` to get the
following full usage description:

```
usage: python3 -m philip_pal [-h] [--verbose] [--dut_reset] [--reset] [port]

positional arguments:
  port         PHiLIP serial port

optional arguments:
  -h, --help   show this help message and exit
  --verbose    Enable more output
  --dut_reset  Reset device-under-test (DUT)
  --reset      Reset PHiLIP MCU
```

To get output use `--verbose`, otherwise commands will silently be executed.

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
