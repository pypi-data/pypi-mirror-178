---
module: maxlog
author: Max Ludden
email: dev@maxludden.com
---


# MaxLog

#### Version 0.2.0

## Instillation

MaxLog is available on PyPi under an MIT License. It is installable via your favorite package manager:

### Pipx <span style="font-size:.6em;">(recommended)</span>

```shell
pipx install maxlog
```

### Pip

```shell└──
pip install maxlog
```

### Poetry

```shell
poetry add maxlog
```

## Usage

Basic usage is very simple:

```python
from maxlog import new_run

log = new_run()
```

It will generate the follow directory and files:

```
.
└── logs
    ├── log.log
    ├── run.txt
    └── verbose.log
```

- `log.txt` is a text file that is used to keep track of runs.

- `log.log` is a log that is filtered to the `INFO` level.

- `verbose.log` is a log that isn't filtered at all.

Every time `new_run` is called, it will generate the above file structure if it does not exist, read the current run number, increment it, record it back to disk, and then clear the console and print the current run number to the console as the tile of a horizontal rule. 

<div style="font-size:.8em;font-align:center;">
    <h2>MIT License</h2>
    <p>Copyright 2022 Maxwell Owen Ludden</span></p>
    <p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p>
    <p>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p>
    <p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</p>
