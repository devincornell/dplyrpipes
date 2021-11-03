
from typing import Callable, Any, Union
import functools

import dataclasses

class CompFunc:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.other_funcs = list()
    
    def __call__(self, input: Any) -> Any:
        '''Actually call function.'''
        x = self.func(input, *self.args, **self.kwargs)
        for other_func in self.other_funcs:
            if not isinstance(other_func, out):
                x = other_func(x)
        return x

    def __rshift__(self, other_compfunc):
        '''Aggregate component functions.
        '''
        self.other_funcs.append(other_compfunc)
        return self
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.func}, {", ".join(map(str,self.args))})'


def comp_decorator(func):
    def wrapper_comp_decorator(*args, **kwargs):
        return CompFunc(func, *args, **kwargs)
    return wrapper_comp_decorator


@dataclasses.dataclass
class CompData:
    data: Any
    def __rshift__(self, compfunc: CompFunc):
        if isinstance(compfunc, out):
            return self.data
        return self.__class__(compfunc(self.data))

class out:
    def __call__(self, *args, **kwargs):
        return None


@comp_decorator
def test_func(x, y: int = 1):
    return x * y


if __name__ == '__main__':
    
    out = CompData(5) >> (
        test_func(2) >> 
        out()
    )
    print(out)

    #print(my_comp(test_func(2)))
    print(type(test_func))
    print(type(test_func()))
    
    comp = test_func(y=5)
    print(comp(2))
    #print(CompData(2) >> test_func)


    # CompData: used to pass data
    # CompFunc: operates on CompData


    #say_whee(lambda x: x == 5)
    #say_whee()
    #say_whee()

    #pipestart(x) &\
    #    myfilt(x = 1)

    #startpipe + x >>\
    #myfilter(lambda x: x * 2)
