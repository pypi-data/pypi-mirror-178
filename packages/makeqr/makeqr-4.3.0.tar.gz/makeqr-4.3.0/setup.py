# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['makeqr']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'pydantic[email]>=1.8.2,<2.0.0',
 'qrcode[pil]>=7.3.1,<8.0.0']

entry_points = \
{'console_scripts': ['makeqr = makeqr.__main__:main']}

setup_kwargs = {
    'name': 'makeqr',
    'version': '4.3.0',
    'description': 'Generate QR cards for any occasion',
    'long_description': '# MakeQR\n\n[![PyPI](https://img.shields.io/pypi/v/makeqr.svg)](https://pypi.python.org/pypi/makeqr)\n[![PyPI](https://img.shields.io/pypi/dm/makeqr.svg)](https://pypi.python.org/pypi/makeqr)\n\nGenerate WiFi Access QR Codes\n\n# Installation\n\n```bash\npip install makeqr -U\n```\n\n## To test that installation was successful, try:\n\n```bash\nmakeqr --help\n```\n\nor\n\n```bash\nmakeqr wifi --help\n```\n\n# Usage example\n\n## Command line command\n\n### Command\n\n```bash\nmakeqr -v wifi --password TopSecret --security wpa2 HomeWiFi\n```\n\n### Output\n\n```plain\n __   __  _______  ___   _  _______  _______  ______\n|  |_|  ||   _   ||   | | ||       ||       ||    _ |\n|       ||  |_|  ||   |_| ||    ___||   _   ||   | ||\n|       ||       ||      _||   |___ |  | |  ||   |_||_\n|       ||       ||     |_ |    ___||  |_|  ||    __  |\n| ||_|| ||   _   ||    _  ||   |___ |      | |   |  | |\n|_|   |_||__| |__||___| |_||_______||____||_||___|  |_|\n\nModel: {"ssid": "HomeWiFi", "security": "wpa2", "password": "TopSecret", "hidden": false}\nEncoded: WIFI:S:HomeWiFi;P:TopSecret;T:WPA;;\n                                                              \n  ██████████████  ████    ██████  ██  ██      ██████████████  \n  ██          ██    ██████████████      ██    ██          ██  \n  ██  ██████  ██      ██      ██    ██████    ██  ██████  ██  \n  ██  ██████  ██  ██████          ██  ██  ██  ██  ██████  ██  \n  ██  ██████  ██  ██    ████          ████    ██  ██████  ██  \n  ██          ██  ██  ████        ██████████  ██          ██  \n  ██████████████  ██  ██  ██  ██  ██  ██  ██  ██████████████  \n                  ████  ██████    ██████                      \n  ██      ██  ██████████    ██  ██████  ██  ██████████    ██  \n  ██    ██      ██    ████  ██████            ████████        \n    ██████████████      ████    ██        ████    ████    ██  \n  ██        ██  ████    ██    ██  ████  ████  ██        ██    \n    ██████    ██    ██      ██████████    ████  ████    ██    \n  ██    ██        ████    ██    ██    ██        ██████        \n  ████████    ████    ████████████  ████      ██      ██  ██  \n            ██  ██      ██  ██  ████████  ████      ██    ██  \n      ██      ██    ██    ████      ██  ██  ██        ██  ██  \n  ██    ██      ██      ████████  ██    ██    ██████████      \n      ██    ████  ████  ██      ████████    ██      ████  ██  \n        ██████  ████████████  ████████  ██    ██  ██          \n  ████    ██  ██  ██      ██████  ██████  ██████████    ██    \n                  ██████  ██      ████    ██      ████  ██    \n  ██████████████  ██        ██████      ████  ██  ██  ██  ██  \n  ██          ██        ██  ██      ████  ██      ████        \n  ██  ██████  ██  ██  ██  ████    ██    ████████████████      \n  ██  ██████  ██              ██  ██    ████        ██    ██  \n  ██  ██████  ██    ██          ████████                ████  \n  ██          ██            ████  ████  ██  ██    ████  ████  \n  ██████████████  ████████    ██████████  ████████  ██  ██    \n                                                              \n```\n\n## Docker container\n\n```bash\ndocker run ghcr.io/shpaker/makeqr:4.0.1 link https://t.me/shpaker\n```\n\n## As python module\n\n```python\nfrom makeqr import MakeQR, QRMailToModel\n\nqr = MakeQR(\n  model = QRMailToModel(\n    to=\'foo@bar.baz\',\n    subject=\'Awesome subject!\',\n  )\n)\ndata: bytes = qr.make_image_data()\n```\n',
    'author': 'Aleksandr Shpak',
    'author_email': 'shpaker@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/shpaker/makeqr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
