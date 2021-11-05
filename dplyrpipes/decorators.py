


def comp_decorator(func):
    def wrapper_comp_decorator(*args, **kwargs):
        func.argdata = args
        func.kwargdata = kwargs
        return func
    return wrapper_comp_decorator

