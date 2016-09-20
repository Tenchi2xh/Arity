# -*- encoding: utf-8 -*-

import random
import pytest

from arity.decorators import *


def factorial(n, accu=1):
    if n == 1:
        return accu
    else:
        return factorial(n-1, n*accu)


def fibonacci(n, a=0, b=1):
    if n == 0:
        return a
    else:
        return fibonacci(n-1, b, a+b)


def quicksort(ls, parent=None):
    if parent is None:
        parent = []
    if len(ls) <= 1:
        return ls + parent
    else:
        pivot = ls[0]
        less, equal, greater = [], [], []
        for e in ls:
            if e < pivot:
                less = [e] + less
            elif e == pivot:
                equal = [e] + equal
            else:
                greater = [e] + greater
        return quicksort(less, equal + quicksort(greater, parent))


random.seed(0)
to_sort_10 = list(range(10))
to_sort_100 = list(range(100))
to_sort_500 = list(range(500))
random.shuffle(to_sort_10)
random.shuffle(to_sort_100)
random.shuffle(to_sort_500)

optimized_factorial = tail_recursive(factorial)
optimized_fibonacci = tail_recursive(fibonacci)
optimized_quicksort = tail_recursive(quicksort)


@pytest.mark.benchmark(group="factorial_10")
def test_recursive_factorial_10(benchmark):
    result = benchmark(factorial, 10)
    assert result == 3628800
@pytest.mark.benchmark(group="factorial_10")
def test_optimized_factorial_10(benchmark):
    result = benchmark(optimized_factorial, 10)
    assert result == 3628800

@pytest.mark.benchmark(group="factorial_100")
def test_recursive_factorial_100(benchmark):
    result = benchmark(factorial, 100)
    assert result == 93326215443944152681699238856266700490715968264381621468592963895217599993229915608941463976156518286253697920827223758251185210916864000000000000000000000000
@pytest.mark.benchmark(group="factorial_100")
def test_optimized_factorial_100(benchmark):
    result = benchmark(optimized_factorial, 100)
    assert result == 93326215443944152681699238856266700490715968264381621468592963895217599993229915608941463976156518286253697920827223758251185210916864000000000000000000000000

@pytest.mark.benchmark(group="factorial_500")
def test_recursive_factorial_500(benchmark):
    result = benchmark(factorial, 500)
    assert result == 1220136825991110068701238785423046926253574342803192842192413588385845373153881997605496447502203281863013616477148203584163378722078177200480785205159329285477907571939330603772960859086270429174547882424912726344305670173270769461062802310452644218878789465754777149863494367781037644274033827365397471386477878495438489595537537990423241061271326984327745715546309977202781014561081188373709531016356324432987029563896628911658974769572087926928871281780070265174507768410719624390394322536422605234945850129918571501248706961568141625359056693423813008856249246891564126775654481886506593847951775360894005745238940335798476363944905313062323749066445048824665075946735862074637925184200459369692981022263971952597190945217823331756934581508552332820762820023402626907898342451712006207714640979456116127629145951237229913340169552363850942885592018727433795173014586357570828355780158735432768888680120399882384702151467605445407663535984174430480128938313896881639487469658817504506926365338175055478128640000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
@pytest.mark.benchmark(group="factorial_500")
def test_optimized_factorial_500(benchmark):
    result = benchmark(optimized_factorial, 500)
    assert result == 1220136825991110068701238785423046926253574342803192842192413588385845373153881997605496447502203281863013616477148203584163378722078177200480785205159329285477907571939330603772960859086270429174547882424912726344305670173270769461062802310452644218878789465754777149863494367781037644274033827365397471386477878495438489595537537990423241061271326984327745715546309977202781014561081188373709531016356324432987029563896628911658974769572087926928871281780070265174507768410719624390394322536422605234945850129918571501248706961568141625359056693423813008856249246891564126775654481886506593847951775360894005745238940335798476363944905313062323749066445048824665075946735862074637925184200459369692981022263971952597190945217823331756934581508552332820762820023402626907898342451712006207714640979456116127629145951237229913340169552363850942885592018727433795173014586357570828355780158735432768888680120399882384702151467605445407663535984174430480128938313896881639487469658817504506926365338175055478128640000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000


@pytest.mark.benchmark(group="fibonacci_10")
def test_recursive_fibonacci_10(benchmark):
    result = benchmark(fibonacci, 10)
    assert result == 55
@pytest.mark.benchmark(group="fibonacci_10")
def test_optimized_fibonacci_10(benchmark):
    result = benchmark(optimized_fibonacci, 10)
    assert result == 55

@pytest.mark.benchmark(group="fibonacci_100")
def test_recursive_fibonacci_100(benchmark):
    result = benchmark(fibonacci, 100)
    assert result == 354224848179261915075
@pytest.mark.benchmark(group="fibonacci_100")
def test_optimized_fibonacci_100(benchmark):
    result = benchmark(optimized_fibonacci, 100)
    assert result == 354224848179261915075

@pytest.mark.benchmark(group="fibonacci_500")
def test_recursive_fibonacci_500(benchmark):
    result = benchmark(fibonacci, 500)
    assert result == 139423224561697880139724382870407283950070256587697307264108962948325571622863290691557658876222521294125
@pytest.mark.benchmark(group="fibonacci_500")
def test_optimized_fibonacci_500(benchmark):
    result = benchmark(optimized_fibonacci, 500)
    assert result == 139423224561697880139724382870407283950070256587697307264108962948325571622863290691557658876222521294125


@pytest.mark.benchmark(group="quicksort_10")
def test_recursive_quicksort_10(benchmark):
    result = benchmark(quicksort, to_sort_10)
    assert result == list(range(10))
@pytest.mark.benchmark(group="quicksort_10")
def test_optimized_quicksort_10(benchmark):
    result = benchmark(optimized_quicksort, to_sort_10)
    assert result == list(range(10))

@pytest.mark.benchmark(group="quicksort_100")
def test_recursive_quicksort_100(benchmark):
    result = benchmark(quicksort, to_sort_100)
    assert result == list(range(100))
@pytest.mark.benchmark(group="quicksort_100")
def test_optimized_quicksort_100(benchmark):
    result = benchmark(optimized_quicksort, to_sort_100)
    assert result == list(range(100))

@pytest.mark.benchmark(group="quicksort_500")
def test_recursive_quicksort_500(benchmark):
    result = benchmark(quicksort, to_sort_500)
    assert result == list(range(500))
@pytest.mark.benchmark(group="quicksort_500")
def test_optimized_quicksort_500(benchmark):
    result = benchmark(optimized_quicksort, to_sort_500)
    assert result == list(range(500))
