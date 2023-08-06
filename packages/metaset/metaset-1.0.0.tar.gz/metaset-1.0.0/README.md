# metaset

This package provides a collection that is basically a "dict of sets", named MetaSet.

![Build status](https://travis-ci.org/Polyconseil/metaset.svg?branch=master)
![Supported Python versions](https://img.shields.io/pypi/pyversions/metaset.svg)
![Wheel status](https://img.shields.io/pypi/wheel/metaset.svg)
![License](https://img.shields.io/pypi/l/metaset.svg)

## Quickstart

Install the package from [PyPI](http://pypi.python.org/pypi/metaset/), using pip:

```
pip install metaset
```

Or from GitHub:

```
$ git clone git://github.com/lionel-panhaleux/metaset.git
```

Import it in your code:

```python
from metaset import MetaSet
```

Usage is quite straight forward,
basic set operations are supported via the binary operators `+` `-` `|` `^`.

```python
>>> MetaSet(a={1, 2}, b={3}) | MetaSet(b={4}, c={5})
{'a': {1, 2}, 'b': {3, 4}, 'c': {5}}
```

## Detailed considerations

They are two ways to consider the "dict of sets" notion,
differing on how you handle the empty values for keys.

The easiest idea is to consider that a key with no content is non-existent.
This is how the [dictset](https://code.google.com/archive/p/dictset/) package is implemented.

In this alternative implementation, we chose to keep the empty keys as meaningful elements,
allowing for smart unions and intersections.

```python
>>> MetaSet(a={1}) | Metaset(a={2}, b=set())
{'a': {1, 2}, 'b': set()}

>>> MetaSet(a={1}) & Metaset(a={2}, b={3})
{'a': set()}
```

So, beware of how empty-keys are handled,
and consider using [dictset](https://code.google.com/archive/p/dictset/)
if it is a better match for your use case.
The behavior for subtraction and symmetric difference,
although sound on a mathematical point of view, may not be what you want.

```python
>>> MetaSet(a={1}) - MetaSet(a={1})
{'a': set()}

>>> MetaSet(a={1}) ^ MetaSet(a={1})
{'a': set()}
```
