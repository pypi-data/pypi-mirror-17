# Browserinfo

> A lightwight python wrapper for [browser-info.net](http://www.browser-info.net/) to retrieve UA strings

[![Build Status](https://travis-ci.org/stylesuxx/browserinfo.svg?branch=master)](https://travis-ci.org/stylesuxx/browserinfo) [![Downloads](https://img.shields.io/pypi/dm/browserinfo.svg)](https://img.shields.io/pypi/dm/browserinfo.svg) [![Documentation Status](https://readthedocs.org/projects/browserinfo/badge/?version=latest)](http://browserinfo.readthedocs.io/en/latest/?badge=latest)

## What does browserinfo do?
It allows you to retrieve user agent strings, sorted by popularity or most recent.

## Usage example
```python
>>> import browserinfo
>>> browserinfo.recent(1)
['Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36\n']
>>> browserinfo.popular(1)
['Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.6.01001)']
```

## Installation
Use pip:

    pip install -U browserinfo

## Building doc
From the root of the directory run:

    sphinx-apidoc -o docs/ browserinfo -f && cd docs && make html && cd ..

## Building Dist Package
To build a distributable package run:

```
python setup.py sdist
```
