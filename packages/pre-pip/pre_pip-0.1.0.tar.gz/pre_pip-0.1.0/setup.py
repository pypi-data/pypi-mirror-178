# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pre_pip']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'rich>=12.6.0,<13.0.0']

entry_points = \
{'console_scripts': ['pre-pip = pre_pip.cli:cli']}

setup_kwargs = {
    'name': 'pre-pip',
    'version': '0.1.0',
    'description': '',
    'long_description': '## Pre-pip\n\n`pre-pip` is a tool that allows you to run something before a pip command is executed.\n\n### Suggested use cases:\n\n- Before installing a package, check it against a list of known malicious packages.\n- Upgrade pip automatically before installing a package.\n\nYou can use it to run any custom python code before a pip command is executed.\n\n### Supported terminals\n\nCurrently only `zsh` is supported.\n\nContributions for other shells are welcome.\n\n### Installation\n\n```sh\npip install pre-pip\n```\n\nThere is potential to make this `pipx` installable.\n\n### Usage\n\nInstall `pre-pip` into your `.*rc` file using:\n\n```sh\npre-pip install\n```\n\n### Register a custom demo hook\n\nCreate a new file called demo_hook.py in your current directory with the following content:\n\n```python\nfrom rich import print as rprint\n\n\ndef main(args):\n    rprint(\n        f"This [italic green]pre-pip[/italic green] hook received: [italic cyan]{args}[/italic cyan]",\n    )\n\n```\n\nRegister the hook using:\n\n```sh\npre-pip register ./demo_hook.py\n```\n\nYou can view the list of registered hooks using:\n\n```sh\npre-pip list\n```\n\n### Uninstall\n\nUninstall `pre-pip` using:\n\n```sh\npre-pip uninstall\n```\n\nThis will remove the `pre-pip` hook from your `.*rc` file as well as all registered hooks.\n\nTo remove the pre-pip package, use:\n\n```sh\npip uninstall pre-pip\n```\n\n### License\n\n[MIT](LICENSE)\n',
    'author': 'Ratul Maharaj',
    'author_email': 'ratulmaharaj@looped.co.za',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
