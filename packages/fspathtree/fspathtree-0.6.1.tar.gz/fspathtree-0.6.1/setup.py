# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fspathtree']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fspathtree',
    'version': '0.6.1',
    'description': 'A small utility for wrapping trees (nested dict/list) that allows filesystem-like path access, including walking up with "../".',
    'long_description': '# FS Path Tree\n\nA simple class to allow filesystem-style path access to nested dict/list structures,\nincluding support for walking "up" the tree with \'..\'.\n\nExample:\n\n```python\n  config = fspathtree()\n  config.update( { \'desc\' : "example config"\n                 , \'time\' : { \'N\' : 50\n                            , \'dt\' : 0.01 }\n                 , \'grid\' : { \'x\' : { \'min\' : 0\n                                    , \'max\' : 0.5\n                                    , \'N\' : 100 }\n                            , \'y\' : { \'min\' : 1\n                                    , \'max\' : 1.5\n                                    , \'N\' : 200 }\n                            }\n                 } )\n\n  # elements are accessed in the same was as a dict.\n  assert config[\'desc\'] == "example config"\n  # sub-elements can also be accessed the same way.\n  assert config[\'grid\'][\'x\'][\'max\'] == 0.5\n  # but they can also be accessed using a path.\n  assert config[\'grid/x/max\'] == 0.5\n\n  # get a sub-element in the tree.\n  x = config[\'grid/x\']\n\n  # again, elements of grid/x are accessed as normal.\n  assert x[\'max\'] == 0.5\n  # but we can also access elements that are not in this branch.\n  assert x[\'../y/max\'] == 1.5\n  # or reference elements from the root of the tree.\n  assert x[\'/time/N\'] == 50\n```\n\n## Install\n\nYou can install the latest release with `pip`.\n```\n$ pip install fspathtree\n```\nOr, even better, using `pipenv`\n```\n$ pipenv install fspathtree\n```\n\n## Design\n\nThe `fspathtree` is a small wrapper class that can wrap any nested tree data structure. The tree that is wrapped can be accessed with\nthe `.tree` attribute. This is an improvement over the old `fspathdict.pdict` class, which stored nodes internally as `fspathdict.pdict` instances\nand required "converting" to and from the standard python dict and list types.\n',
    'author': 'CD Clark III',
    'author_email': 'clifton.clark@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
