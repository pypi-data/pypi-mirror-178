# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kedro_databricks']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'kedro-databricks',
    'version': '0.0.1',
    'description': 'Kedro plugin with Databricks support',
    'long_description': '# Kedro Databricks plugin\n\n[![Python Version](https://img.shields.io/pypi/pyversions/kedro-databricks)](https://github.com/getindata/kedro-databricks)\n[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![SemVer](https://img.shields.io/badge/semver-2.0.0-green)](https://semver.org/)\n[![PyPI version](https://badge.fury.io/py/kedro-databricks.svg)](https://pypi.org/project/kedro-databricks/)\n[![Downloads](https://pepy.tech/badge/kedro-databricks)](https://pepy.tech/project/kedro-databricks)\n\n[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=getindata_kedro-databricks&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=getindata_kedro-databricks)\n[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=getindata_kedro-databricks&metric=coverage)](https://sonarcloud.io/summary/new_code?id=getindata_kedro-databricks)\n[![Documentation Status](https://readthedocs.org/projects/kedro-databricks/badge/?version=latest)](https://kedro-databricks.readthedocs.io/en/latest/?badge=latest)\n\n<p align="center">\n  <a href="https://getindata.com/solutions/ml-platform-machine-learning-reliable-explainable-feature-engineering"><img height="150" src="https://getindata.com/img/logo.svg"></a>\n  <h3 align="center">We help companies turn their data into assets</h3>\n</p>\n\n# Coming soon!\nStay tuned or connect with us directly.\n\n',
    'author': 'GetInData MLOPS',
    'author_email': 'mlops@getindata.com',
    'maintainer': 'GetInData MLOPS',
    'maintainer_email': 'mlops@getindata.com',
    'url': 'https://github.com/getindata/kedro-databricks',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
