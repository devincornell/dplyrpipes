
import functools

def component(func):
    def wrapper_component(*args, **kwargs):
        func.argdata = args
        func.kwargdata = kwargs
        return func
        #return functools.partial(func, *args, **kwargs)
    return wrapper_component
    #return functools.partial()
