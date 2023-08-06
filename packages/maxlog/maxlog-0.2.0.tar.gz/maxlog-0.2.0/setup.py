# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['maxlog']
install_requires = \
['loguru>=0.6.0,<0.7.0',
 'maxcolor>=1.0.0,<2.0.0',
 'maxconsole>=0.4.0,<0.5.0',
 'maxprogress>=0.4.0,<0.5.0',
 'myaml>=1.0.1,<2.0.0',
 'rich[all]>=12.6.0,<13.0.0']

setup_kwargs = {
    'name': 'maxlog',
    'version': '0.2.0',
    'description': 'Helper module for logging using Loguru sinks.',
    'long_description': '---\nmodule: maxlog\nauthor: Max Ludden\nemail: dev@maxludden.com\n---\n\n\n# MaxLog\n\n#### Version 0.2.0\n\n## Instillation\n\nMaxLog is available on PyPi under an MIT License. It is installable via your favorite package manager:\n\n### Pipx <span style="font-size:.6em;">(recommended)</span>\n\n```shell\npipx install maxlog\n```\n\n### Pip\n\n```shell└──\npip install maxlog\n```\n\n### Poetry\n\n```shell\npoetry add maxlog\n```\n\n## Usage\n\nBasic usage is very simple:\n\n```python\nfrom maxlog import new_run\n\nlog = new_run()\n```\n\nIt will generate the follow directory and files:\n\n```\n.\n└── logs\n    ├── log.log\n    ├── run.txt\n    └── verbose.log\n```\n\n- `log.txt` is a text file that is used to keep track of runs.\n\n- `log.log` is a log that is filtered to the `INFO` level.\n\n- `verbose.log` is a log that isn\'t filtered at all.\n\nEvery time `new_run` is called, it will generate the above file structure if it does not exist, read the current run number, increment it, record it back to disk, and then clear the console and print the current run number to the console as the tile of a horizontal rule. \n\n<div style="font-size:.8em;font-align:center;">\n    <h2>MIT License</h2>\n    <p>Copyright 2022 Maxwell Owen Ludden</span></p>\n    <p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p>\n    <p>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p>\n    <p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</p>\n',
    'author': 'maxludden',
    'author_email': 'dev@maxludden.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
