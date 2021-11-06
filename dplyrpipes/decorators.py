
import functools

def component(func):
    def wrapper_component(*args, **kwargs):
        func.argdata = args
        func.kwargdata = kwargs
        return func
    return wrapper_component
