# Stirling

[![Documentation Status](https://readthedocs.org/projects/stirling/badge/?version=latest)](https://stirling.readthedocs.io/en/latest/?badge=latest)

![CI](https://github.com/rob-smallshire/stirling/actions/workflows/actions.yml/badge.svg)


[![codecov](https://codecov.io/gh/rob-smallshire/stirling/branch/master/graph/badge.svg?token=66QU3UW6N3)](https://codecov.io/gh/rob-smallshire/stirling)

## Installation

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

## CI/CD

    $ bumpversion patch
    $ git push --follow-tags