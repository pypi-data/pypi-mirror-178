# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['etsi_qkd_014_client']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['qkd014-client = etsi_qkd_014_client.cli:main']}

setup_kwargs = {
    'name': 'etsi-qkd-014-client',
    'version': '0.9.0',
    'description': 'A Python client for the QKD 014 standard',
    'long_description': "# etsi_qkd_014_client\n\nThe ETSI GS QKD 014 specification is a specification for communication between a client and a QKD module to retrieve cryptographic keys that have been exchanged using a Quantum Key Distribution protocol.\n\nThe specifications can be found at the following address : <https://www.etsi.org/deliver/etsi_gs/QKD/001_099/014/01.01.01_60/gs_qkd014v010101p.pdf>\n\nThe current version of the software uses the version V1.1.1 of the specifications (version from 2019-02).\n\n## Features\n\n* Connect to a QKD server, using a custom CA, key and cert;\n* Retrieve status of the QKD server with the `get_status` command;\n* Retrieve a secure key using the `get_key` command;\n* Retrieve a secure key knowing the key's ID using the `get_key_with_key_IDs` command.\n## Documentation\n\nThe full documentation can be found at https://etsi-qkd014-client.readthedocs.io/en/latest/.\n\n## License\n\nThis software is distributed under the GNU Lesser General Public License v3 ([GNU LGPLv3](https://www.gnu.org/licenses/lgpl-3.0.en.html)). A copy of the complete text of the license is included with the software (the LICENSE file).\n\nThe header of the license can be found below :\n\n> Copyright (C) 2022 Yoann Piétri\n> Copyright (C) 2022 LIP6 - Sorbonne Université\n>\n> etsi-qkd-14-client is free software: you can redistribute it and/or modify\n> it under the terms of the GNU Lesser General Public License as published > by\n> the Free Software Foundation, either version 3 of the License, or\n> (at your option) any later version.\n>\n> etsi-qkd-14-client is distributed in the hope that it will be useful,\n> but WITHOUT ANY WARRANTY; without even the implied warranty of\n> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n> GNU Lesser General Public License for more details.\n>\n> You should have received a copy of the GNU Lesser General Public License\n> along with etsi-qkd-14-client. If not, see <http://www.gnu.org/licenses>.\n\n## Citation\n\nIf you use this software, please consider citation. Here is the biblatex entry :\n\n```latex\n@software{etsi_qkd_014_client,\n  author = {{Yoann Piétri}},\n  title = {ETSI QKD 014 client},\n  url = {https://github.com/nanoy42/etsi_qkd_014_client},\n  version = {0.1.1},\n  date = {2022-06-02},\n}\n```\n\nIf `@software` is not available, you can also use\n\n```latex\n@misc{etsi_qkd_014_client,\n  author = {{Yoann Piétri}},\n  title = {ETSI QKD 014 client},\n  url = {https://github.com/nanoy42/etsi_qkd_014_client},\n  date = {2022-06-02},\n}\n```\n\nPlain text citation :\n\n> Yoann Piétri. (2022). ETSI QKD 014 client (0.1.1) [Computer software]. <https://github.com/nanoy42/etsi_qkd_014_client>\n",
    'author': 'Yoann Piétri',
    'author_email': 'Yoann.Pietri@lip6.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nanoy42/etsi-qkd-014-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4',
}


setup(**setup_kwargs)
