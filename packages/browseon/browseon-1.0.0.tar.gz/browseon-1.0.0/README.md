# browseon

[![PyPI](https://img.shields.io/pypi/v/browseon)](https://pypi.python.org/pypi/browseon)
[![Pypi - License](https://img.shields.io/github/license/codesrg/browseon)](https://github.com/codesrg/browseon/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/browseon?color=red)](https://pypi.python.org/pypi/browseon)

To browse web.

## Installation

`pip install -U browseon`

## Usage

```
usage: browseon [options]

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show version number and exit.

to browse web:
  -q , --query    query to search
  -u , --url      url to open
  -e , --engine   search engine to search (Optional)
```

### Python Script

To browse web.

```python
from browseon import browse

browse.open('scheme://sub-domain.domain.top-level-domain/')  # to open url
browse.search("pypi browseon")  # to search query
```

### Command Line

To search in web browser.

```
$ browseon --query "pypi browseon"
```

## Issues:

If you encounter any problems, please file an [issue](https://github.com/codesrg/browseon/issues) along with a detailed
description.