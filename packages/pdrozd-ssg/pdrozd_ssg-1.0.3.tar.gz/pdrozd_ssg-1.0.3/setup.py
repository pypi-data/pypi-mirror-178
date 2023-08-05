# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['SSG', 'SSG.tests', 'SSG.utils']

package_data = \
{'': ['*'], 'SSG.tests': ['testFiles/*']}

install_requires = \
['Markdown>=3.4.1,<4.0.0',
 'Poetry>=1.2.2,<2.0.0',
 'black>=22.10.0,<23.0.0',
 'flake8>=5.0.4,<6.0.0']

entry_points = \
{'console_scripts': ['pdrozd = SSG:main']}

setup_kwargs = {
    'name': 'pdrozd-ssg',
    'version': '1.0.3',
    'description': 'P-DR0ZD-SSG',
    'long_description': '# pdrozd-ssg\n\npdrozd-ssg is a static site generator created in python\n\n# Features\n * Creates an index based on your html files created\n * Added JSON config file support \n * Complete Markdown Support with the Help of [Python-Markdown/markdown](https://github.com/Python-Markdown/markdown)\n\n# Requirements\n\nPython 3\n\n# How to Install\n\ngo to https://pypi.org/project/pdrozd-ssg/ or simply run the command `pip install pdrozd-ssg` to run use the command?\n\n# Commands\n\nThe commands of pdrozd-ssg are\n* -h or --help this will display to the user the options they have\n\n* -c or --config this will specify a config file which contains arguments for SSG to read.\n\n* -v or --version this will display to the user the current verison of pdrozd-ssg\n\n* -i or --input this with a combanation of .txt or .md file or directory will output your files as a Static Site\n  to use put in the format. e.g. <br>\n   ```py ssg.py -i or --input [file.txt\\text.ms] or [directory\\]``` \n\n* -l or --lang this at the end of the input command will allow the default language of the HTML files to change. e.g.<br>\n   ```py ssg.py -i or --input [file.txt\\text.md] or [directory\\] -l or --lang [language]```\n\n# Config File\nConfig files should be in legal JSON format with a similar format like\n``` \n{\n    "input":"./Sherlock-Holmes-Selected-Stories",\n    "lang":"fr"\n} \n```\n\n # New features\n\n',
    'author': 'P-DR0ZD',
    'author_email': '60482468+P-DR0ZD@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
