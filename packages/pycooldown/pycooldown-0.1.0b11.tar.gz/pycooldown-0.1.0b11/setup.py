# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycooldown']

package_data = \
{'': ['*']}

install_requires = \
['mypy-extensions>=0.4.3,<0.5.0']

setup_kwargs = {
    'name': 'pycooldown',
    'version': '0.1.0b11',
    'description': 'A lightning fast cooldown/ratelimit implementation.',
    'long_description': '# pycooldown\n[![pypi](https://github.com/TrigonDev/apgorm/actions/workflows/pypi.yml/badge.svg)](https://pypi.org/project/pycooldown)\n\n[Documentation](https://github.com/circuitsacul/pycooldown/wiki) | [Support](https://discord.gg/dGAzZDaTS9)\n\nA lightning-fast cooldown/ratelimit implementation.\n\n## Example Usage\n```py\nfrom pycooldown import FixedCooldown\n\n\ncooldown = FixedCooldown(period=10, capacity=5)\n\n\ndef handle_event(sender):\n    retry_after = cooldown.update_ratelimit(sender)\n    if retry_after is None:\n        print("Event succeeded!")\n    else:\n        print(f"Too many events from {sender}. Retry in {retry_after} seconds.")\n```\n',
    'author': 'Circuit',
    'author_email': 'circuitsacul@icloud.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/TrigonDev/pycooldown',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
