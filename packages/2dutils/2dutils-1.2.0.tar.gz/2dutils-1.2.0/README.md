# 2D Utils

[![PyPI release](https://github.com/erlete/2dutils/actions/workflows/python-publish.yml/badge.svg)](https://github.com/erlete/2dutils/actions/workflows/python-publish.yml)

A collection of 2D utilities for coordinate representation and manipulation.

## Features

The following features are currently implemented:

* `Coordinate2D` - A custom 2D coordinate representation based on the built-in `tuple` class, but with extended functionality.
* `Circumcenter` - A class for calculating the circumcenter and circumradius of three coordinates.

## Installation

### macOS/UNIX

```bash
git clone https://github.com/erlete/2d-utils
```

**Note: this package is not yet available on PyPI, but it will be really soon.**

## Usage

Once the package has been installed, its modules can be easily imported into custom programs via the `import` statement.

```python
from coordinate import Coordinate2D
from circumcenter import Circumcenter
```
