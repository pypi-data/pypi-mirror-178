# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nx']

package_data = \
{'': ['*']}

install_requires = \
['randomname>=0.1.5,<0.2.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['nx = nx.main:app']}

setup_kwargs = {
    'name': 'nx-nix',
    'version': '1.0.0',
    'description': 'A fast and beautiful NixOS and Nix management utility',
    'long_description': "# NX \n\nA fast and beautiful NixOS and Nix management utility ❄\n\n\n## 💡 Features\n\n- Beautiful and powerful CLI using Python's [typer](https://typer.tiangolo.com/) library\n- Quick and easy deployment and management of NixOS systems and Nix profiles\n\n\n## 💾 Installation\n\n### 💽 From Binary\n\n**Install NX using `nix profile`**\n```bash\n  $ nix profile install gitlab:mchal_/nx\n  $ nx\n```\n\n## 📸 Screenshots\n\n![NX Screenshot](https://media.discordapp.net/attachments/1014738924515635302/1046919833339568208/image.png)\n\n## 📜 License\n\n[GPLv3-only](https://choosealicense.com/licenses/gpl-3.0/)\n",
    'author': 'Michal',
    'author_email': 'mchal_@tuta.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
