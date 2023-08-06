# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['javascript-runner']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['jsRunner = javascript-runner.javascript-runner:cli']}

setup_kwargs = {
    'name': 'javascript-runner',
    'version': '0.1.0',
    'description': 'Run Nodejs from Python',
    'long_description': '# Node.py\n\nRun nodejs from python\n\n## Features\n\n- Runs: .js, .ts, .mjs and .cjs files.\n- Supports all npm libraries\n- Automatically compiles .ts files and runs them with NO tsconfig (uses tsc)\n- No dependencies\n- Uses modern api\n\n## Installation\n\n',
    'author': 'micziz',
    'author_email': 'miczicontent@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
