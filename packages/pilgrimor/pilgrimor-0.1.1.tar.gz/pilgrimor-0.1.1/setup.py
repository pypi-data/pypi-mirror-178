# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pilgrimor',
 'pilgrimor.abc',
 'pilgrimor.cli',
 'pilgrimor.engine',
 'pilgrimor.migrator',
 'pilgrimor.migrator.python_migrator',
 'pilgrimor.migrator.rawsql_migrator']

package_data = \
{'': ['*'], 'pilgrimor': ['.github/workflows/*']}

install_requires = \
['importlib-metadata>=4.12.0,<5.0.0',
 'psycopg-binary>=3.1.4,<4.0.0',
 'psycopg-c>=3.1.4,<4.0.0',
 'psycopg>=3.1.4,<4.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'tomlkit>=0.11.1,<0.12.0']

entry_points = \
{'console_scripts': ['pilgrimor = pilgrimor.__main__:main']}

setup_kwargs = {
    'name': 'pilgrimor',
    'version': '0.1.1',
    'description': '',
    'long_description': '# pilgrimor\nDatabase migration tool with versioning\nfor python projects\n\n## Installation:\n\n### with pip\n```\npip install pilgrimor\n```\n\n### with poetry\n```\npoetry add pilgrimor\n```\n\n## Usage:\n\n### Main commands:\n* `initdb` - create technical migrations table.\n* `apply` - apply new migrations.\n* `apply —-version <version number>` - apply new migrations with version.\n* `rollback —-version <version number>`- rollback migrations to version inclusive.\n* `rollback —-latest` - rollback to latest version.\n\n### Necessary things\nYou need to specify some fields in your pyproject.toml\n```\n[tool.pilgrimor]\nmigrations_dir = "./migrations/"\ndatabase_engine = "PSQL"\nenv_file = "./.env"\n```\nmigrations_dir - folder with migrations\ndatabase_engine - there is only one database engine PSQL\nenv_file = path to .env file\n\n### Migration file structure:\nMigration file contains two blocks - apply and rollback with sql commands.\nFor example:\n```\n—- apply —-\nSQL CODE\n\n—- rollback —-\nSQL CODE\n```\n\n',
    'author': 'Kiselev Aleksandr',
    'author_email': 'askiselev00@gmail.com',
    'maintainer': 'Kiselev Aleksandr',
    'maintainer_email': 'askiselev00@gmail.com',
    'url': 'https://github.com/pilgrimor/pilgrimor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
