# Gadm-connector

![Supported Versions](https://img.shields.io/pypi/pyversions/gadm-connector)
![Version](https://img.shields.io/pypi/v/gadm-connector?label=package%20version)
![Downloads](https://img.shields.io/pypi/dm/gadm-connector)
![Status](https://img.shields.io/pypi/status/gadm-connector)

Simple donwloader for gadm border data.

```python

import gadm

Netherlands = gadm.Country("NLD", 0, "4.1")

```

## Installing

Gadm-connector is available on PyPI:

```console
python -m pip install gadm-connector
```

Gadm-connector is build for python 3.8+.

## Features

* get geopandas dataframe of country borders
* get list of coordinates of country borders
