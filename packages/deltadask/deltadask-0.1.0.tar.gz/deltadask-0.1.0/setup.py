# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deltadask']

package_data = \
{'': ['*']}

install_requires = \
['dask==2022.10.2', 'deltalake==0.6.3']

setup_kwargs = {
    'name': 'deltadask',
    'version': '0.1.0',
    'description': '',
    'long_description': '# deltadask\n\nA connector for reading Delta Lake tables into Dask DataFrames.\n\nInstall with `pip install deltadask`.\n\nRead a Delta Lake into a Dask DataFrame as follows:\n\n```python\nimport deltadask\n\nddf = deltadask.read_delta("path/to/delta/table")\n```\n\n## Basic usage\n\nSuppose you have a Delta table with the following three versions.\n\n![Delta table with version](https://github.com/MrPowers/deltadask/blob/main/images/delta-table-with-versions.png)\n\nHere\'s how to read the latest version of the Delta table:\n\n```python\ndeltadask.read_delta("path/to/delta/table").compute()\n```\n\n```\n   id\n0   7\n1   8\n2   9\n```\n\nAnd here\'s how to read version 1 of the Delta table:\n\n```python\ndeltadask.read_delta("path/to/delta/table", version=1).compute()\n```\n\n```\n   id\n0   0\n1   1\n2   2\n3   4\n4   5\n```\n\nDelta Lake makes it easy to time travel between different versions of a Delta table with Dask.\n\nSee this notebook for a full working example with an environment so you can replicate this on your machine.\n\n## Why Delta Lake is better than Parquet for Dask\n\nA Delta table stores data in Parquet files and metadata in a trasaction log.  The metadata includes the schema and location of the files.\n\n![Delta table architecture](https://github.com/MrPowers/deltadask/blob/main/images/delta-table.png)\n\nA Dask Parquet data lake can be stored in two different ways.\n\n1. Parquet files with a single metadata file\n2. Parquet files without a metadata file\n\nParquet files with a single metadata file are limited because a single file has scaling limitations.\n\nParquet files without a metadata file are limited because they require a relatively expensive file listing operation followed by calls to build the overall metadata statistics for the data lake.\n\nDelta Lake is better because the transaction log is scalable and can be queried a lot faster than an expensive file listing operation.\n\nHere\'s an example of how to query a Delta table with Dask and take advantage of column pruning and predicate pushdown filtering:\n\n```python\nddf = deltadask.read_delta(\n    "path/to/delta/table", \n    columns=["col1"], filters=[[(\'col1\', \'==\', 0)]])\n```\n\n## Why this library is really easy to build\n\nReading a Delta Lake into a Dask DataFrame is ridiculously easy, thanks to [delta-rs](https://github.com/delta-io/delta-rs/).\n\nReading Delta Lakes is also really fast and efficient.  You can get a list of the files from the transaction log which is a lot faster than a file listing operation.\n\nYou can also skip entire files based on column metadata stored in the transaction log.  Skipping data allows for huge performance improvements.\n\nHere\'s how to read a Delta Lake into a Dask DataFrame with this library:\n',
    'author': 'Matthew Powers',
    'author_email': 'matthewkevinpowers@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
