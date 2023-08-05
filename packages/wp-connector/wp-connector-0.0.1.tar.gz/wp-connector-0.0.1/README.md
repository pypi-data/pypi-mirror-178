# Wp-connector

![Supported Versions](https://img.shields.io/pypi/pyversions/wp-connector)
![Version](https://img.shields.io/pypi/v/wp-connector?label=package%20version)
![Downloads](https://img.shields.io/pypi/dm/wp-connector)
![Status](https://img.shields.io/pypi/status/wp-connector)

Simple donwloader for wp population data.

```python

import wp

Client = wp.WP()

Client.to_pandas("NLD", "ppp_2020")

```

## Installing

Wp-connector is available on PyPI:

```console
python -m pip install wp-connector
```

Wp-connector is build for python 3.8+.

## Features

* download raster data from WorldPop Server
* format data to pandas dataframe
