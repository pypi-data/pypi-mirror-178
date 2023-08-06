# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eml2md']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['eml2md = eml2md._main:main']}

setup_kwargs = {
    'name': 'eml2md',
    'version': '0.1.2',
    'description': 'Convert from eml file to markdown text.',
    'long_description': '# eml2md\n\n[![codecov](https://codecov.io/gh/elda27/eml2md/branch/main/graph/badge.svg?token=Ck30XyeFvG)](https://codecov.io/gh/elda27/eml2md)\n\n`eml2md` is a command line tool for converting from eml to markdown.\n\n## Example\n\n```bash\neml2md -i tests/example/Test.eml -o Test.md\n```\n\n```markdown\n|         |                                                                          |\n| ------- | ------------------------------------------------------------------------ |\n| From    | 井炉波鳰惠土 <author2@example.com>                                       |\n| To      | 井炉波鳰惠土 <author1@example.com><br>井炉波鳰惠土 <author2@example.com> |\n| CC      | 井炉波鳰惠土 <author2@example.com><br> <author1@example.com>             |\n| Date    | 2022-08-09 23:47:29                                                      |\n| Subject | Re: Test                                                                 |\n\ntest blanks\n2022 年 8 月 9 日(火) 23:47 井炉波鳰惠土 <author1@example.com>:\n\n> Quote message\n>\n> dsadbubfdus[\\\n> dsadinadioa\n>\n> dsnaidnai\n>\n> dsnuandi\n```\n\n## Usage\n\n```bash\nusage: eml2md [-h] -i INPUT -o OUTPUT [-f {simple,html}]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -i INPUT, --input INPUT\n                        Input file\n  -o OUTPUT, --output OUTPUT\n                        Output file\n  -f {simple,html}, --format {simple,html}\n                        Format of output markdown\n```\n',
    'author': 'elda27',
    'author_email': 'kaz.birdstick@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/elda27/eml2md',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
