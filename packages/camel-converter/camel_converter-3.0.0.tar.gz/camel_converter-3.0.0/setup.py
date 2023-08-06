# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['camel_converter']

package_data = \
{'': ['*']}

extras_require = \
{'pydantic': ['pydantic>=1.8.2']}

setup_kwargs = {
    'name': 'camel-converter',
    'version': '3.0.0',
    'description': 'Converts a string from snake case to camel case or camel case to snake case',
    'long_description': '# Camel Converter\n\n[![CI Status](https://github.com/sanders41/camel-converter/workflows/CI/badge.svg?branch=main&event=push)](https://github.com/sanders41/camel-converter/actions?query=workflow%3CI+branch%3Amain+event%3Apush)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sanders41/camel-converter/main.svg)](https://results.pre-commit.ci/latest/github/sanders41/camel-converter/main)\n[![Coverage](https://codecov.io/github/sanders41/camel-converter/coverage.svg?branch=main)](https://codecov.io/gh/sanders41/camel-converter)\n[![PyPI version](https://badge.fury.io/py/camel-converter.svg)](https://badge.fury.io/py/camel-converter)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/camel-converter?color=5cc141)](https://github.com/sanders41/camel-converter)\n\nIn JSON keys are frequently in camelCase format, while variable names in Python are typically\nsnake_case. The purpose of this pacakgae is to help convert between the two formats.\n\n## Usage\n\n- To convert from camel case to snake case:\n\n  ```py\n  from camel_converter import to_snake\n\n  snake = to_snake("myString")\n  ```\n\n  This will convert `myString` into `my_string`\n\n- To convert a dictonary\'s keys from camel case to snake case:\n\n  ```py\n  from camel_converter import dict_to_snake\n\n  snake = dict_to_snake({"myString": "val 1"})\n  ```\n\n  This will convert `{"myString": "val 1"}` into `{"my_string": "val 1"}`. Non-string keys will be\n  left unchanged.\n\n  This is also available as a decorator for functions that return a dictionary.\n\n  ```py\n  from camel_converter.decorators import dict_to_snake\n\n  @dict_to_snake\n  def my_func() -> dict[str, str]:\n      return {"myString": "val 1"}\n\n  snake = my_func()\n  ```\n\n  `my_func` will return `{"my_string": "val 1"}`. Non-string keys will be\n  left unchanged.\n\n- To convert from snake case to camel case:\n\n  ```py\n  from camel_converter import to_camel\n\n  camel = to_camel("my_string")\n  ```\n\n  This will convert `my_string` into `myString`\n\n- To convert from a dictionary\'s keys from snake case to camel case:\n\n  ```py\n  from camel_converter import dict_to_camel\n\n  camel = to_camel({"my_string": "val 1"})\n  ```\n\n  This will convert `{"my_string": "val 1"}` into `{"myString": "val 1"}` Non-string keys will be\n  left unchanged.\n\n  This is also available as a decorator for functions that return a dictionary.\n\n  ```py\n  from camel_converter.decorators import dict_to_camel\n\n  @dict_to_camel\n  def my_func() -> dict[str, str]:\n      return {"my_string": "val 1"}\n\n  camel = my_func()\n  ```\n\n  `my_func` will return `{"myString": "val 1"}`. Non-string keys will be\n  left unchanged.\n\n- To convert from snake to pascal case:\n\n  ```py\n  from camel_converter import to_pascal\n\n  pascal = to_pascal("my_string")\n  ```\n\n  This will convert `my_string` into `MyString`\n\n- To convert from a dictionary\'s keys from snake case to pascal case:\n\n  ```py\n  from camel_converter import dict_to_pascal\n\n  pascal = to_pascal({"my_string": "val 1"})\n  ```\n\n  This will convert `{"my_string": "val 1"}` into `{"MyString": "val 1"}` Non-string keys will be\n  left unchanged.\n\n  This is also available as a decorator for functions that return a dictionary.\n\n  ```py\n  from camel_converter.decorators import dict_to_pascal\n\n  @dict_to_pascal\n  def my_func() -> dict[str, str]:\n      return {"my_string": "val 1"}\n\n  pascal = my_func()\n  ```\n\n  `my_func` will return `{"MyString": "val 1"}`. Non-string keys will be\n  left unchanged.\n\n### Optional Extras\n\nAn optional extra is provided for [Pydantic](https://pydantic-docs.helpmanual.io/) that provides a\nbase class to automatically convert between snake case and camel case. To use this Pydantic class\ninstall camel converter with:\n\n```sh\npip install camel-converter[pydantic]\n```\n\nThen your Pydantic classes can inherit from CamelBase.\n\n```py\nfrom camel_converter.pydantic_base import CamelBase\n\n\nclass MyModel(CamelBase):\n    test_field: str\n\n\nmy_data = MyModel(**{"testField": "my value"})\nprint(my_data.test_field)\n```\n\nwill result in `my value` being printed.\n\nWith setting up your model in this way `myField` from the source, i.e. JSON data, will map to `my_field` in your model.\n\n## Contributing\n\nIf you are interesting in contributing to this project please see our [contributing guide](CONTRIBUTING.md)\n',
    'author': 'Paul Sanders',
    'author_email': 'psanders1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sanders41/camel-converter',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
