# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypassrs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pypassrs',
    'version': '0.5.5',
    'description': 'Python wrapper for passrs',
    'long_description': '# pypassrs\n\nA Python wrapper around [passrs](https://crates.io/projects/passrs)\n\n## Usage\n\n```py\nfrom pypassrs import pypassrs\n\n# Initialize a new password storage\npypassrs.init(".passrs_storage")\n\n# Generate a new password\npassword = pypassrs.generate()\n\n# Insert the new password into the storage\npypassrs.insert("path/to/password", password)\n\n# Alternatively, store the password that is generated\npypassrs.generate("path/to/password2")\n\n# Get a password\npypassrs.show("path/to/password")\n\n# Show password directory\nprint(pypassrs.tree())\n```\n',
    'author': 'Casey Burklow',
    'author_email': 'zevaryx@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
