<img src="https://raw.githubusercontent.com/edgarsi/strstrdict/main/docs/_static/logo.png" alt="logo" width="100" align="right"/>

![PyPI - License](https://img.shields.io/pypi/l/strstrdict.svg?style=flat-square)
![Tests](https://github.com/edgarsi/strstrdict/workflows/Run%20tests/badge.svg)


# strstrdict 

Low memory overhead alternative to Python's `dict`, with string keys and values.

Uses half of the memory of `dict` for strings of length 40, at the cost of being
half as fast. More improvement at shorter strings, less at longer ones. See more
at [benchmarks](#benchmarks).


## 📝 Documentation

Drop-in replacement for `dict` with the following limitations:
* Only supports string keys and values.
* Iterating order is unspecified.
* Any modification invalidates iterators.

```
>>> from strstrdict import StrStrDict

>>> d = StrStrDict()
>>> d['foo'] = 'bar'
>>> d['foo']
'bar'
```
To KISS, this project only supports a string to string dictionary.

More:
* [Implementation details](https://github.com/edgarsi/strstrdict/tree/main/docs/memory.rst)
* [Contributing](https://github.com/edgarsi/strstrdict/tree/main/docs/contrib/index.rst)


## 🐍 Installation

```bash
pip install strstrdict
```


## 📈 Benchmarks<a id="benchmarks"></a>

Filling a dictionary with 1m items, key and value strings
**5-10 chars** long, from a
pool of 2m random strings. Then reading values 1m
times, with a 50% hit rate.

|                      | Fill time (s)   | Read time (s)   | Memory (MB)   |
|----------------------|-----------------|-----------------|---------------|
| dict                 | **0.19s**       | **0.17s**       | 159.60        |
| sqlitedict[^wrapper] | 10.31s          | 51.79s          | 69.41         |
| strstrdict           | 0.41s           | 0.44s           | **64.44**     |


Filling a dictionary with 1m items, key and value strings
**20-30 chars** long, from a
pool of 2m random strings. Then reading values 1m
times, with a 50% hit rate.

|                      | Fill time (s)   | Read time (s)   | Memory (MB)   |
|----------------------|-----------------|-----------------|---------------|
| dict                 | **0.26s**       | **0.21s**       | 193.23        |
| sqlitedict[^wrapper] | 9.17s           | 41.09s          | 139.40        |
| strstrdict           | 0.41s           | 0.42s           | **95.38**     |


Filling a dictionary with 1m items, key and value strings
**100-200 chars** long, from a
pool of 2m random strings. Then reading values 1m
times, with a 50% hit rate.

|                      | Fill time (s)   | Read time (s)   | Memory (MB)   |
|----------------------|-----------------|-----------------|---------------|
| dict                 | **0.38s**       | **0.24s**       | 447.02        |
| sqlitedict[^wrapper] | 11.31s          | 42.62s          | 572.88        |
| strstrdict           | 0.76s           | 0.56s           | **344.73**    |

[^wrapper]: SqliteDict is used with commiting every 1000 writes. Note that
SqliteDict is not intended for in-memory storage, but still has great efficiency
at short strings.


## 🙏 Thanks & Credits

[parallel-hashmap](https://github.com/greg7mdp/parallel-hashmap) for their amazing header-only library!

[pysimdjson](https://github.com/TkTech/pysimdjson) for a reference how to write a cython lib!
