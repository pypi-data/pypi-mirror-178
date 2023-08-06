from base import profile, start


def f(x):
    return x*x + 1


@profile()
def list_func1():
    xs = [i for i in range(0, 100_000)]
    k = [f(x) for x in xs]
    return k


@profile()
def list_func2():
    xs = [i for i in range(0, 100_000)]
    k = list(map(f, xs))
    return k


@profile()
def list_func3():
    xs = [i for i in range(0, 100_000)]
    k = [*map(f, xs)]
    return k

@profile()
def list_func4():
    xs = [i for i in range(0, 100_000)]
    k = [x*x+1 for x in xs]
    return k


@profile()
def list_func5():
    xs = [i for i in range(0, 100_000)]
    k = list(map(lambda x: x*x+1, xs))
    return k

if __name__ == '__main__':
    start(__file__, __name__, locals())
