# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_dbx']

package_data = \
{'': ['*']}

install_requires = \
['dbx>=0.8.7,<0.9.0',
 'delta-spark==2.1.1',
 'ipython>=8.5.0,<9.0.0',
 'pytest>=7.1.3,<8.0.0']

entry_points = \
{'pytest11': ['pytest_dbx = pytest_dbx.fixtures']}

setup_kwargs = {
    'name': 'pytest-dbx',
    'version': '0.1.0',
    'description': 'Pytest plugin to run unit tests for dbx (Databricks CLI extensions) related code',
    'long_description': "# pytest-dbx\n\nPytest plugin for testing [dbx](https://github.com/databrickslabs/dbx)-based projects.\n\n## Install\n\nTo use the fixtures in your project, simply add `pytest-dbx` to your project's dev-dependencies\n(where you would place all your test and build dependencies).\n\n## Fixtures\n\nIn unit tests you can use the `dbx_spark` fixture to have a spark session available as in Databricks\n\n```python\ndef test_function(dbx_spark):\n    sdf = dbx_spark.createDataFrame([[1], [2], [3]], ['a'])\n    assert sdf.count() == 3\n```\n\nThe `dbutils_fixture` and `mlflow_local` are automatically used.\n",
    'author': 'Jeroen Meidam',
    'author_email': 'j.meidam@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jmeidam/pytest-dbx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
