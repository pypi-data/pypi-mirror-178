# GRIP4-connector

![Supported Versions](https://img.shields.io/pypi/pyversions/grip4-connector)
![Version](https://img.shields.io/pypi/v/grip4-connector?label=package%20version)
![Downloads](https://img.shields.io/pypi/dm/grip4-connector)
![Status](https://img.shields.io/pypi/status/grip4-connector)

Simple donwloader for gadm border data.

```python

import grip4

EU = grip4.Region("Europe")
DUTCH_ROADS = EU.get_roads("NLD")

```

## Installing

Grip4-connector is available on PyPI:

```console
python -m pip install grip4-connector
```

Grip4-connector is build for python 3.8+.

## Features

* get geopandas dataframe of region roads
* get geopandas dataframe of country roads
