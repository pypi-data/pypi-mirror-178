# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['teamtime']

package_data = \
{'': ['*']}

install_requires = \
['geopy>=2.3.0,<3.0.0',
 'pandas>=1.5.2,<2.0.0',
 'plotly>=5.11.0,<6.0.0',
 'prettytable>=3.5.0,<4.0.0',
 'pytz>=2022.6,<2023.0']

entry_points = \
{'console_scripts': ['teamtime = teamtime.teamtime:main']}

setup_kwargs = {
    'name': 'teamtime',
    'version': '2.0.0.post1',
    'description': 'A tool for keeping track of staff in multiple timezones',
    'long_description': "Note: As of 10/13 I asked in the snapcraft forum to have the ownership of the snap changed to joesecurity . Thanks for checking roadmr.\n\n# teamTime\n----\n\nteamTime is a tool to aid the problem of keeping track of time for a globally distributed team.\n\nYou will need to put the name of your teammates in staff.csv using the format name, timezone, city. Take a look at https://raw.githubusercontent.com/joemcmanus/teamTime/master/example.csv\n\n    Alice,US/Eastern,New York New York\n    Bob,US/Central,Chicago Illinois\n    Charlie,Africa/Abidjan, Abidjan\n    Doug,America/Tijuana, Tijuana Mexico\n    Ed,America/Winnipeg, Winnipeg\n    Frank,Asia/Dubai,Dubai\n\nQuestions/Feedback/Feature Requests? Please let me know.\n\n# Installation\n----\n\n## Snap\nTo install teamTime as a snap, type:\n\n    sudo snap install teamtime\n\n## pip\n\nTo install teamTime with pip, type:\n\n\tpip install teamtime\n\n## To install and run from source\n\nInstall the requirements:\n\n\tpip install -r requirements.txt\n\tpython -m teamtime.teamtime\n\n## Note\n\nTo avoid typing the path to the CSV file you might want to make an alias:\n\n    alias teamtime='teamtime --src=/home/foo/staff.csv'\n\n\n# Usage\n----\n\n    teamtime --help\n    usage: teamtime [-h] [--name NAME] [--src SRC] [--map]\n\n    Time Table\n\n    optional arguments:\n      -h, --help   show this help message and exit\n      --name NAME  Optional name to search for\n      --comp COMP  Compare times, use --name and --comp together\n      --src SRC    Optional src file, defaults to staff.csv\n      --map        Draw map\t\n\nTo simply print a table of your team run `teamtime`\n\n    +---------+------------------+\n    |  Person |    Local Time    |\n    +---------+------------------+\n    |  Alice  | 2019-09-25 12:16 |\n    |   Bob   | 2019-09-25 11:16 |\n    | Charlie | 2019-09-25 16:16 |\n    |   Doug  | 2019-09-25 09:17 |\n    |    Ed   | 2019-09-25 11:17 |\n    |  Frank  | 2019-09-25 20:17 |\n    |  now()  | 2019-09-25 10:16 |\n    +---------+------------------+\n\nTo search for just Bob run `teamtime --name=Bob`\n\n    +--------+------------------+\n    | Person |    Local Time    |\n    +--------+------------------+\n    | Bob    | 2019-10-02 15:37 |\n    +--------+------------------+\n\nTo convert a local time to another time in a person's time zone use --comp. This helps when you are trying to figure out when to schedule a call.\n\n    $ teamtime --name=andy --comp=15:00\n    +--------+------------------+---------------------+\n    | Person |    Their Time    |      Your Time      |\n    +--------+------------------+---------------------+\n    |  Andy  | 2019-10-18 07:30 | 2019-10-17 15:00:00 |\n    +--------+------------------+---------------------+\n\nTo create a map run `teamtime --map`\n\n![alt_tag](https://github.com/joemcmanus/teamTime/blob/master/map.png)\n",
    'author': 'Joe McManus',
    'author_email': 'josephmc@alumni.cmu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mssalvatore/teamTime',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
