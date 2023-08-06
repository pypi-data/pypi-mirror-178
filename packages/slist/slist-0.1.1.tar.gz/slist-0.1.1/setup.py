# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slist', 'tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'slist',
    'version': '0.1.1',
    'description': 'A typesafe list with more method chaining!',
    'long_description': '# Slist\nA spruced up version of the built-in python list.\n\nMore post-fixed methods for lovely chaining!\n\nLeverage the latest mypy features to spot errors during coding.\n\nAll these methods return a new list. They do not mutate the original list.\n\n\n[![pypi](https://img.shields.io/pypi/v/slist.svg)](https://pypi.org/project/slist)\n[![python](https://img.shields.io/pypi/pyversions/slist.svg)](https://pypi.org/project/slist)\n[![Build Status](https://github.com/thejaminator/slist/actions/workflows/dev.yml/badge.svg)](https://github.com/thejaminator/slist/actions/workflows/dev.yml)\n\n```\npip install slist\n```\n\n\n* GitHub: <https://github.com/thejaminator/slist>\n\n\n## Quick Start\nWith mypy installed, easily spot errors when you call the wrong methods on your sequence.\n\n```python\nfrom slist import Slist\n\nmany_strings = Slist(["Lucy, Damion, Jon"])  # Slist[str]\nmany_strings.sum()  # Mypy errors with \'Invalid self argument\'. You can\'t sum a sequence of strings!\n\nmany_nums = Slist([1, 1.2])\nassert many_nums.sum() == 2.2  # ok!\n\nclass CannotSortMe:\n    def __init__(self, value: int):\n        self.value: int = value\n\nstuff = Slist([CannotSortMe(value=1), CannotSortMe(value=1)])\nstuff.sort_by(lambda x: x)  # Mypy errors with \'Cannot be "CannotSortMe"\'. There isn\'t a way to sort by the class itself\nstuff.sort_by(lambda x: x.value)  # ok! You can sort by the value\n\nSlist([{"i am a dict": "value"}]).distinct_by(\n    lambda x: x\n)  # Mypy errors with \'Cannot be Dict[str, str]. You can\'t hash a dict itself\n```\n\nSlist provides methods that you can chain easily for easier data processing.\n```python\nfrom slist import Slist\n\ntest = Slist([-1, 0, 1]).map(\n    lambda x: x if x >= 0 else None\n).flatten_option()  # Mypy infers slist[int] correctly\n```\n',
    'author': 'James Chua',
    'author_email': 'chuajamessh@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/thejaminator/slist',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
