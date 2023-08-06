# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hntpy']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['sandbox = hntpy.sandbox:sandbox']}

setup_kwargs = {
    'name': 'hntpy',
    'version': '0.0.6',
    'description': 'Python wrapper for Helium API to simplify interactions with the Helium blockchain.',
    'long_description': '# hntpy\n\n<p align="left">\n    <a alt="Version" href="https://pypi.org/project/hntpy/">\n    <img src="https://img.shields.io/badge/version-0.0.6-blue"/></a>\n    <a href="https://github.com/h-morgan/hntpy/blob/main/LICENSE" alt="License">\n    <img src="https://img.shields.io/github/license/h-morgan/hntpy"/></a>\n    <a alt="Coverage" href="#">\n    <img src="https://img.shields.io/badge/coverage-92%25-green"/></a>\n</p>\n\n## Introduction\n\nPython wrapper for Helium API to simplify interaction with Helium blockchain. The aim of this project is to enable retrieval of Helium data from the API in a Pythonic way.\n\nFor more detail on exact API responses/data, please see the officical [Helium documentation](https://docs.helium.com/api/blockchain/introduction).\n\nThis project is continually under development. If you notice a bug, or have a feature request, please submit a Github issue [here](https://github.com/h-morgan/hntpy/issues).\n\n## Install\n\nTo use the latest version of this Python package, download from PyPi:\n\n```\npip install hntpy\n```\n\n## Usage\n\n### The Account module\n\nThe `Account` module allows you to interact with/get data about your Helium account in a simplified way.\n\n[Official Helium Accounts API documentation](https://docs.helium.com/api/blockchain/accounts).\n\nTo instantiate an Account instance for your Helium account:\n\n```python\nfrom hntpy import Accounts\n\n# pass your 51-digit Helium account/wallet address\naccount = Account("your-helium-account-addr-here")\n\n# your Helium account address will be stored/accessible here\naddr = account.account_id\n```\n\nTo retrieve your account details:\n\n```python\ndetails = account.get_account_details()\n```\n\n#### List hotspots and validators for an account\n\nThe `details` variable is now a python `dict` containing your account details from the Helium API.\n\nTo get a list of hotspots, and their data, for your account:\n\n```python\nhotposts = account.hotspots()\n```\n\nThe `hotspots` variable is now a list of hotspots and their data, for example:\n\n```\n[\n    {\n      "lng": -81.70707772367822,\n      "lat": 41.480133219396784,\n      "status": {\n        "online": "online",\n        "height": 435166,\n        "gps": "good_fix"\n      },\n      "score_update_height": 435153,\n      "score": 0.9222412109375,\n      "owner": "13GCcF7oGb6waFBzYDMmydmXx4vNDUZGX4LE3QUh8eSBG53s5bx",\n      "nonce": 1,\n      "name": "sneaky-violet-penguin",\n      "location": "8c2ab38f19a43ff",\n      "geocode": {\n        "short_street": "W 32nd St",\n        "short_state": "OH",\n        "short_country": "US",\n        "short_city": "Cleveland",\n        "long_street": "West 32nd Street",\n        "long_state": "Ohio",\n        "long_country": "United States",\n        "long_city": "Cleveland",\n        "city_id": "Y2xldmVsYW5kb2hpb3VuaXRlZCBzdGF0ZXM"\n      },\n      "block_added": 96087,\n      "block": 435241,\n      "address": "1182nyT3oXZPMztMSww4mzaaQXGXd5T7JwDfEth6obSCwwxxfsB"\n    }\n  ]\n```\n\nTo get a list of the validators, and their data, associated with your account:\n\n```python\nvalidators = account.validators()\n```\n\n#### OUIS and roles for an account\n\nFor OUIs and roles, these endpoints sometimes return large amounts of data that take a while to retrieve from the Helium API. For these methods, you have the option of requesting how you want the data returned to you, either:\n\n- list format\n- generator of batches of lists\n\nIf you\'d like to wait and receive one giant list of data, simply run:\n\n```python\n# to get ouis for your account\nouis = account.ouis()\n\n# to get roles for your account\nroles = account.roles()\n```\n\n**Note:** Depending on the amount of data these requests have to return, you may need to wait a bit while the reqeuests complete. In instances where there are many pages of data being returned from the Helium API, these requests can sometimes take minutes.\n\nIf you\'d like to return batches of lists, using a generator, for each page of data retrieved from the API, simply pass the `gen=True` argument:\n\n```python\n# to get ouis for your account\nouis = account.ouis(gen=True)\n\n# to get roles for your account\nroles = account.roles(gen=True)\n```\n\nYou can then iterate over these variables like you would any Python generator, to view your data in batches. For example:\n\n```python\nfor batch in roles:\n    ## batch is now a list of role items returned from Helium\n    for role in batch:\n        hash_id = role["hash"]\n        # ...\n```\n\nTo get the role counts (transaction/activity counts) for an account:\n\n```python\nrole_counts = account.role_counts()\n```\n',
    'author': 'Haley Morgan',
    'author_email': 'haleymorgan3264@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/h-morgan/hntpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
