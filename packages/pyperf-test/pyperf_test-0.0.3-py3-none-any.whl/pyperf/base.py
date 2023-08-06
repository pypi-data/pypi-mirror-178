import time
from functools import wraps
import inspect

decorated = {}


def profile(number: int = 100):
    def _profile(func):
        modname = inspect.getmodule(inspect.stack()[1][0]).__name__
        if modname not in decorated:
            decorated[modname] = []
        decorated[modname].append(func.__name__)

        @wraps(func)
        def wrapper(*args, **kwargs):
            all_time = 0.0
            for _ in range(number):
                start = time.perf_counter()
                func(*args, **kwargs)
                end = time.perf_counter()
                all_time += end - start
            all_time /= number
            print(f'Time for \'{func.__name__} [{number}]\': {all_time: .4f} ms.')
            return all_time

        return wrapper
    return _profile

def start(_path, _name_list,  _locals):
    import pathlib
    print(f'### Test: {{{pathlib.Path(_path).resolve().name.split(sep=".")[0]}}} ###')
    from statistics import mean
    r = {}
    for _name in _name_list:
        for name in decorated.get(_name, []):
            attr = _locals[name]
            ret = attr()
            r[name] = ret

    min_name = min(r, key=r.get)
    min_value = r[min_name]
    del r[min_name]
    m = mean(r.values())
    print(f'- [{min_name}]: {int(100 - min_value * 100 / m)}% less')