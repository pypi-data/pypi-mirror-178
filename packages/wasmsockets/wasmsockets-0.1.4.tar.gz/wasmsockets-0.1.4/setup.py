# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wasmsockets']

package_data = \
{'': ['*']}

extras_require = \
{':sys_platform != "emscripten"': ['websockets>=10.4,<11.0']}

setup_kwargs = {
    'name': 'wasmsockets',
    'version': '0.1.4',
    'description': 'Async interface to Pyodide WebSockets',
    'long_description': 'wasmsockets\n===========\n\nThis is a thin layer over the pyodide JS WebSocket interface. It is intended \nto provide a similar interface to the `websockets` python package.\n\nThis package will only work when run under the pyodide environment.\n',
    'author': 'dek',
    'author_email': 'dek@substructure.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/SubstructureOne/wasmsockets',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
