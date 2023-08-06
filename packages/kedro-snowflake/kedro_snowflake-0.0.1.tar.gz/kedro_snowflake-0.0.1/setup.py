# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kedro_snowflake']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'kedro-snowflake',
    'version': '0.0.1',
    'description': 'Kedro plugin with Snowflake / Snowpark support',
    'long_description': '# Kedro Snowflake Pipelines plugin\n\n[![Python Version](https://img.shields.io/pypi/pyversions/kedro-snowflake)](https://github.com/getindata/kedro-snowflake)\n[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![SemVer](https://img.shields.io/badge/semver-2.0.0-green)](https://semver.org/)\n[![PyPI version](https://badge.fury.io/py/kedro-snowflake.svg)](https://pypi.org/project/kedro-snowflake/)\n[![Downloads](https://pepy.tech/badge/kedro-snowflake)](https://pepy.tech/project/kedro-snowflake)\n\n[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=getindata_kedro-snowflake&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=getindata_kedro-snowflake)\n[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=getindata_kedro-snowflake&metric=coverage)](https://sonarcloud.io/summary/new_code?id=getindata_kedro-snowflake)\n[![Documentation Status](https://readthedocs.org/projects/kedro-snowflake/badge/?version=latest)](https://kedro-snowflake.readthedocs.io/en/latest/?badge=latest)\n\n<p align="center">\n  <a href="https://getindata.com/solutions/ml-platform-machine-learning-reliable-explainable-feature-engineering"><img height="150" src="https://getindata.com/img/logo.svg"></a>\n  <h3 align="center">We help companies turn their data into assets</h3>\n</p>\n\n# Coming soon!\nStay tuned or connect with us directly.\n\n',
    'author': 'GetInData MLOPS',
    'author_email': 'mlops@getindata.com',
    'maintainer': 'GetInData MLOPS',
    'maintainer_email': 'mlops@getindata.com',
    'url': 'https://github.com/getindata/kedro-snowflake',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
