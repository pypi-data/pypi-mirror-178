# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tlvdict']

package_data = \
{'': ['*']}

install_requires = \
['pyobjict']

setup_kwargs = {
    'name': 'tlvdict',
    'version': '1.1.0',
    'description': 'A Python dict that handles TLV decode/encode, very useful for EMV Data.',
    'long_description': '![](https://github.com/311labs/objict/workflows/tests/badge.svg)\n\n## TLV - Type/Tag Length Format\n\nSimple class that supports TLV encoding/decoding.\n\n\n## Simple to use!\n\n```python\n>>> from tlvdict import TLVDict\n>>> tlv = TLVDict.FromDict({"5F25": "200531", "9F06": "A0000000041010"})\n>>> tlv\nTLVDict([(\'5F25\', \'200531\'), (\'9F06\', \'A0000000041010\')])\n>>> tlv.build()\n\'5F25032005319F0607A0000000041010\'\n\n>>> tlv2 = TLVDict.FromHex("5F25032005319F0607A0000000041010")\n>>> tlv2\nTLVDict([(\'5f25\', \'200531\'), (\'9f06\', \'A0000000041010\')])\n\n```\n\n\n',
    'author': 'Ian Starnes',
    'author_email': 'ians@311labs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
