# -*- encoding: utf-8 -*-

import pytest

from arity.decorators import *


def test_tail_recursion_detection():
    @tail_recursive
    def foo(n):
        if n == 10:
            return
        else:
            return foo(n-1)

    with pytest.raises(RuntimeError):
        @tail_recursive
        def bar(n):
            if n == 0:
                return
            else:
                return bar(n-1), bar(n-1)

    with pytest.raises(RuntimeError):
        @tail_recursive
        def baz(n):
            if n == 0:
                return
            else:
                return baz(n-1) + 1

    with pytest.raises(RuntimeError):
        @tail_recursive
        def b4r(n):
            if n == 0:
                return
            else:
                return int(n-1) + 1


def test_tail_recursion_optimization():
    import inspect
    reference = len(inspect.stack())
    
    def foo(n):
        if n == 1:
            return len(inspect.stack()) 
        else:
            return foo(n-1)

    optimized_foo = tail_recursive(foo)

    assert foo(10) - reference == 10
    assert optimized_foo(10) - reference == 1


def test_outer_scope():
    foo = 1337

    @tail_recursive
    def bar(n):
        if n == 1:
            return foo
        return bar(n-1)

    assert bar(10) == foo


def test_ternary():
    @tail_recursive
    def b4z(n):
        return 3 + 3 if n == 1 else b4z(n-1)
