# Stirling

![CI](https://github.com/rob-smallshire/stirling/actions/workflows/actions.yml/badge.svg)


## Installation

The `stirling` package is available on the Python Package Index (PyPI):

[![PyPI version](https://badge.fury.io/py/stirling.svg)](https://badge.fury.io/py/stirling)

Stirling should work with Python 3.8 or greater. To install:

    $ pip install stirling


## Examples

A function for generating partitions of a collection into a specific number of
non-empty subsets. The number of ways of arranging a set of size n into k non-empty subsets is known at the [Stirling Number of the Second Kind](https://en.wikipedia.org/wiki/Stirling_numbers_of_the_second_kind) 
or S(n, k).

For example, to find the arrangements of a list of 4 integers into 3 non-empty
subsets, use:

    >>> from stirling import k_subsets
    >>> for arrangement in k_subsets([1, 2, 3, 4], 3):
    ...    print(arrangement)
    ...
    [[1, 2], [3], [4]]
    [[1, 3], [2], [4]]
    [[1], [2, 3], [4]]
    [[1, 4], [2], [3]]
    [[1], [2, 4], [3]]
    [[1], [2], [3, 4]]

To determine the number of arrangements of a set of 10 items into 5 non-empty subsets, use
the `s2` function:

    >>> from stirling import s2
    >>> s2(10, 5)
    42525
