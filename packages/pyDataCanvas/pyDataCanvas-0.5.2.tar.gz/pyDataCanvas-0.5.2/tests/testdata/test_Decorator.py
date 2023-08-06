# -*- coding=utf-8 -*-


from functools import wraps
def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Calling decorated function...')
        return func(*args, **kwargs)
  #  return wrapper  @my_decorator


def example():
    """Docstring"""
    print('Called example function')
print(example.__name__, example.__doc__)