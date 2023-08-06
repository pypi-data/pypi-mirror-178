# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bolt_raycast']

package_data = \
{'': ['*'], 'bolt_raycast': ['modules/*']}

install_requires = \
['beet>=0.80.1,<0.81.0', 'bolt>=0.21.0,<0.22.0', 'mecha>=0.61.0,<0.62.0']

setup_kwargs = {
    'name': 'bolt-raycast',
    'version': '0.1.1',
    'description': 'Easily generate raycasting functions for your datapack using bolt',
    'long_description': '# bolt-raycast\n\n[![GitHub Actions](https://github.com/vdvman1/bolt-raycast/workflows/CI/badge.svg)](https://github.com/vdvman1/bolt-raycast/actions)\n\n> Easily generate raycasting functions for your datapack using bolt\n\n## Installation\n\nThe package can be installed with `pip`. Note, you must have `beet`, `mecha` and `bolt` installed to use this package.\n\n```bash\npip install bolt_raycast\n```\n\n---\n\nLicense - [MIT](https://github.com/vdvman1/bolt-raycast/blob/main/LICENSE)\n\n',
    'author': 'Stefan van der Velden',
    'author_email': 'vdvman1@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vdvman1/bolt-raycast',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
