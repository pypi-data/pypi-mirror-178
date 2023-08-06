# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['usb_devices']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'usb-devices',
    'version': '0.4.0',
    'description': 'Tools for mapping, describing, and resetting USB devices',
    'long_description': '# USB Devices\n\n<p align="center">\n  <a href="https://github.com/bluetooth-devices/usb-devices/actions?query=workflow%3ACI">\n    <img src="https://img.shields.io/github/workflow/status/bluetooth-devices/usb-devices/CI/main?label=CI&logo=github&style=flat-square" alt="CI Status" >\n  </a>\n  <a href="https://usb-devices.readthedocs.io">\n    <img src="https://img.shields.io/readthedocs/usb-devices.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">\n  </a>\n  <a href="https://codecov.io/gh/bluetooth-devices/usb-devices">\n    <img src="https://img.shields.io/codecov/c/github/bluetooth-devices/usb-devices.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">\n  </a>\n</p>\n<p align="center">\n  <a href="https://python-poetry.org/">\n    <img src="https://img.shields.io/badge/packaging-poetry-299bd7?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAASCAYAAABrXO8xAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAJJSURBVHgBfZLPa1NBEMe/s7tNXoxW1KJQKaUHkXhQvHgW6UHQQ09CBS/6V3hKc/AP8CqCrUcpmop3Cx48eDB4yEECjVQrlZb80CRN8t6OM/teagVxYZi38+Yz853dJbzoMV3MM8cJUcLMSUKIE8AzQ2PieZzFxEJOHMOgMQQ+dUgSAckNXhapU/NMhDSWLs1B24A8sO1xrN4NECkcAC9ASkiIJc6k5TRiUDPhnyMMdhKc+Zx19l6SgyeW76BEONY9exVQMzKExGKwwPsCzza7KGSSWRWEQhyEaDXp6ZHEr416ygbiKYOd7TEWvvcQIeusHYMJGhTwF9y7sGnSwaWyFAiyoxzqW0PM/RjghPxF2pWReAowTEXnDh0xgcLs8l2YQmOrj3N7ByiqEoH0cARs4u78WgAVkoEDIDoOi3AkcLOHU60RIg5wC4ZuTC7FaHKQm8Hq1fQuSOBvX/sodmNJSB5geaF5CPIkUeecdMxieoRO5jz9bheL6/tXjrwCyX/UYBUcjCaWHljx1xiX6z9xEjkYAzbGVnB8pvLmyXm9ep+W8CmsSHQQY77Zx1zboxAV0w7ybMhQmfqdmmw3nEp1I0Z+FGO6M8LZdoyZnuzzBdjISicKRnpxzI9fPb+0oYXsNdyi+d3h9bm9MWYHFtPeIZfLwzmFDKy1ai3p+PDls1Llz4yyFpferxjnyjJDSEy9CaCx5m2cJPerq6Xm34eTrZt3PqxYO1XOwDYZrFlH1fWnpU38Y9HRze3lj0vOujZcXKuuXm3jP+s3KbZVra7y2EAAAAAASUVORK5CYII=" alt="Poetry">\n  </a>\n  <a href="https://github.com/ambv/black">\n    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="black">\n  </a>\n  <a href="https://github.com/pre-commit/pre-commit">\n    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">\n  </a>\n</p>\n<p align="center">\n  <a href="https://pypi.org/project/usb-devices/">\n    <img src="https://img.shields.io/pypi/v/usb-devices.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">\n  </a>\n  <img src="https://img.shields.io/pypi/pyversions/usb-devices.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">\n  <img src="https://img.shields.io/pypi/l/usb-devices.svg?style=flat-square" alt="License">\n</p>\n\nusb_devices\n\n## Installation\n\nInstall this via pip (or your favourite package manager):\n\n`pip install usb-devices`\n\n## Usage\n\n```\n# python3 examples/info.py\nhci0 manufacturer: Realtek, product: Bluetooth 5.1 Radio, vendor_id: 0bda, product_id: a725, bus_id: 1, dev_num: 11\nhci1 manufacturer: Realtek, product: Bluetooth Radio, vendor_id: 2550, product_id: 8761, bus_id: 1, dev_num: 8\nhci2 manufacturer: Realtek, product: Bluetooth Radio, vendor_id: 2550, product_id: 8761, bus_id: 1, dev_num: 7\nhci3 manufacturer: Realtek, product: Bluetooth Radio, vendor_id: 2550, product_id: 8761, bus_id: 1, dev_num: 4\nhci4 not found\nhci5 not found\nhci6 not found\nhci7 not found\nhci8 not found\n# python3 examples/reset.py\nReset of hci0 succeeded\n```\n\n## Contributors ✨\n\nThanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):\n\n<!-- prettier-ignore-start -->\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- markdownlint-disable -->\n<!-- markdownlint-enable -->\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n<!-- prettier-ignore-end -->\n\nThis project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!\n\n## Credits\n\nThis package was created with\n[Copier](https://copier.readthedocs.io/) and the\n[browniebroke/pypackage-template](https://github.com/browniebroke/pypackage-template)\nproject template.\n',
    'author': 'J. Nick Koston',
    'author_email': 'nick@koston.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bluetooth-devices/usb-devices',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
