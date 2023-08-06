# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rpi_remote']

package_data = \
{'': ['*']}

install_requires = \
['paramiko>=2.12.0,<3.0.0', 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['rpi-remote = rpi_remote.rpi_remote:main']}

setup_kwargs = {
    'name': 'rpi-remote',
    'version': '0.1.5',
    'description': 'Rpi remote client',
    'long_description': '# Rpi Remote client\n\n## Installation\n\n### Prerequisites\n* rust\n* libffi\n* poetry\n* gcc\n* openssl\n\n### Install package\n```\npython3 -m pip install --upgrade rpi-remote --user\n```\n\n### Create service\n```\necho "[Unit]\nDescription=rpi_remote service\nAfter=multi-user.target\nConflicts=getty@tty1.service\n[Service]\nUser=${USER}\nType=simple\nEnvironment="LC_ALL=C.UTF-8"\nEnvironment="LANG=C.UTF-8"\nExecStart=${HOME}/.local/bin/rpi-remote\nRestart=on-failure\n[Install]\nWantedBy=multi-user.target" | sudo tee /etc/systemd/system/rpi-remote.service\n```\n```\nsudo systemctl daemon-reload\nsudo systemctl enable rpi-remote.service\nsudo systemctl start rpi-remote.service\n```\n\n## Edit config\nConfig file path: *~/.config/rpi_remote/config.ini*\n\n## Check logs\n```\njournalctl -f | grep rpi-remote\n```',
    'author': 'Radics Aron',
    'author_email': 'radics.aron.jozsef@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
