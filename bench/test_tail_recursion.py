# -*- encoding: utf-8 -*-

import pytest

from arity.decorators import *


def factorial(n, accu=1):
    if n == 1:
        return accu
    else:
        return factorial(n-1, n*accu)


optimized = tail_recursive(factorial)


@pytest.mark.benchmark(group="factorial_100")
def test_recursive_factorial_100(benchmark):
    benchmark(factorial, 100)


@pytest.mark.benchmark(group="factorial_100")
def test_optimized_factorial_100(benchmark):
    benchmark(optimized, 100)
