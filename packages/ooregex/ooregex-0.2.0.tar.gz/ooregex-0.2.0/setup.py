# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ooregex']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ooregex',
    'version': '0.2.0',
    'description': 'A simple, object-oriented, regular expression generator.',
    'long_description': '<h1 align="center">\nooregex\n</h1>\n\n![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/TitaniumBrain/ooregex?sort=semver)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/ooregex?color=orange&label=%E2%AC%87%20downloads)\n![GitHub](https://img.shields.io/github/license/TitaniumBrain/ooregex?color=blue)\n![Code Style - Black](https://img.shields.io/badge/code%20style-black-000000.svg)\n\nA simple, object oriented, regular expression generator.\n\n`ooregex` is a package aimed at providing a simple syntax for composing\nregular expressions, without having to memorise their syntax.\n\nIt **does not** guarantee that the expressions generated are the most efficient.\n\nIt is assumed that users have some understanding of [regular expressions](https://docs.python.org/3/library/re.html), as there\'s nothing preventing invalid expressions from being generated.\n\n*This project most likely still needs more testing, so I won\'t bump it to version 1.0 until I\'m sure it\'s good enough.*\n\n## Installation\n\nYou can install this package using pip with the command\n\n```bash\npip install ooregex\n```\n\n## Usage\n\nThe main purpose of this package is generating regular expressions to be used in other projects, for example, with the built-in re module.\n\nSee the full documentation [here](docs/tutorial.md).\n\nImport the module with:\n\n```python\nimport ooregex\n```\n\nAlternatively, import only the symbols that you need:\n\n```python\nfrom ooregex import (...)\n```\n\nNow let\'s build an expression for matching a price tag:\n\n```python\nimport re\n\nfrom ooregex import *\n\npattern = Regex(\n    Group(name="price", expression=Regex(\n        DIGIT[1:],\n        Optional(DOT + DIGIT[:]))\n        ),\n    Group(name="currency", expression=\n        AnyOf("$£€")\n        ),\n)\n# (?P<price>\\d+(?:\\.\\d*)?)(?P<currency>[$£€])\n\ntest_str = "Sales! Everything for 9.99£!"\n\nprice_tag = re.search(str(pattern), test_str)\n\nif price_tag is not None:\n    price = price_tag.group("price")\n    currency = price_tag.group("currency")\n\n    print(price, currency)\n    # 9.99 £\n```\n\nLet\'s examine the pattern:\n\nWe have 2 groups:\n* a group named "price" consisting of:\n    * one or more digits\n    * optionally:\n        * a dot\n        * zero or more digits\n* a group named "currency" consisting of:\n    * any character from "$£€"\n\nLook how much clearer it is compared to the generated string:\n`(?P<price>\\d+(?:\\.\\d*)?)(?P<currency>[$£€])`\n\n## Report a bug\n\nIf you find a bug, you can [open an issue](https://github.com/TitaniumBrain/ooregex/issues) or [email me](mailto:titaniumbrain@vivaldi.net?subject=(ooregex)%20Bug%20Report).\n\n\n## License\n\nThis package is available under the [MIT license](https://choosealicense.com/licenses/mit/).\n',
    'author': 'Titanium Brain',
    'author_email': 'titaniumbrain@vivaldi.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/TitaniumBrain/ooregex',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
