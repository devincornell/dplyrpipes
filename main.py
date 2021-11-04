
from typing import Callable, Any, Union, List
import functools

import dataclasses


############################### Component Classes ###############################

class CompFunc:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.other_compfuncs = list()

    @property
    def is_null(self):
        return self.func is None

    def __call__(self, data: Any) -> Any:
        '''Call self.func on the data.
        '''
        return self.func(data, *self.args, **self.kwargs)

    def execute_all(self, compdata, inplace: bool = False):
        '''Execute all functions on the input data sequentially.
        '''
        all_compfuncs = [self] + self.other_compfuncs

        x = compdata.data
        for compfunc in all_compfuncs:
            if not compfunc.is_null:
                x = compfunc(x)
            else:
                return x

        if inplace:
            compdata.data = x
            return compdata
        else:
            return compdata.__class__(x)

    def __rshift__(self, other_compfunc):
        '''Aggregate component functions.
        '''
        self.other_compfuncs.append(other_compfunc)
        return self
    
    def __repr__(self):
        argstr = ", ".join(map(str,self.args))
        kwargstr = ", ".join(f'{k}={v}' for k,v in self.kwargs.items())
        return f'{self.__class__.__name__}({self.func}, {argstr}, {kwargstr})'

class out(CompFunc):
    '''Used at the end of a pipeline to output data.'''
    def __init__(self):
        super().__init__(func=None)
    def __rshift__(self, other_compfunc):
        raise ValueError('Cannot pipe data after the out().')

@dataclasses.dataclass
class CompData:
    '''Store data and overload operator to apply component functions.'''
    data: Any

    def __rshift__(self, compfunc):
        return compfunc.execute_all(self)

def comp_decorator(func):
    def wrapper_comp_decorator(*args, **kwargs):
        return CompFunc(func, *args, **kwargs)
    return wrapper_comp_decorator


###################### dplyr equivalent overloads ####################

@comp_decorator
def filter(df, *args, **kwargs):
    return df.query(*args, **kwargs)

@comp_decorator
def select(df, *colnames):
    return df[list(colnames)]

@comp_decorator
def arrange(df, *colnames, **kwargs):
    return df.sort_values(colnames, **kwargs)

@comp_decorator
def rename(df, *args, **kwargs):
    return df.rename(*args, **kwargs)

@comp_decorator
def mutate(df, *args, **kwargs):
    return df.assign(*args, **kwargs)

@comp_decorator
def summary(df, *args, **kwargs):
    return df.describe(*args, **kwargs)

@comp_decorator
def passthrough(x):
    return x

if __name__ == '__main__':
    import pandas as pd
    df = pd.DataFrame([
        {'name': 'Karl', 'age': 7}, 
        {'name': 'Sandra', 'age': 10}, 
        {'name': 'Chris', 'age': 12},
        {'name': 'Andreas', 'age': 12},
        {'name': 'Hong', 'age': 50},
    ])

    data = CompData(df) >> (
        mutate(birthyear = 2021-df['age']) >>
        filter('age >= 10') >>
        select('name', 'birthyear') >>
        rename({'birthyear': 'birth_year'}) >>
        out()
    )
    print(data)

