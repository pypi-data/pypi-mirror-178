# Stirling

[![Documentation Status](https://readthedocs.org/projects/stirling/badge/?version=latest)](https://stirling.readthedocs.io/en/latest/?badge=latest)

![CI](https://github.com/rob-smallshire/stirling/actions/workflows/actions.yml/badge.svg)


[![codecov](https://codecov.io/gh/rob-smallshire/stirling/branch/master/graph/badge.svg?token=66QU3UW6N3)](https://codecov.io/gh/rob-smallshire/stirling)

## Installation

    $ pip install stirling


## Examples

A collection of utility functions for processing iterable series which
aren't in [itertools](https://docs.python.org/3/library/itertools.html) or [more-itertools](https://more-itertools.readthedocs.io). Some are little more than simple aliases with less confusing names.

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

## CI/CD

    $ bumpversion patch
    $ git push --follow-tags