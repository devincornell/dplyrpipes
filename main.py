
from typing import Callable, Any, Union, List
import functools

import dataclasses
class out:
    pass

@dataclasses.dataclass
class CompData:
    '''Store data and overload operator to apply component functions.'''
    data: Any

    def __rshift__(self, func: Callable):
        '''Apply a callable on the right to the data.
        '''
        if isinstance(func, out):
            return self.data

        if hasattr(func, 'argdata') and hasattr(func, 'kwargdata'):
            return self.__class__(func(self.data, *func.argdata, **func.kwargdata))
        else:
            return self.__class__(func(self.data))

def comp_decorator(func):
    def wrapper_comp_decorator(*args, **kwargs):
        func.argdata = args
        func.kwargdata = kwargs
        return func
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


def regularfunc(df):
    return df['name']

if __name__ == '__main__':
    import pandas as pd
    df = pd.DataFrame([
        {'name': 'Karl', 'age': 7}, 
        {'name': 'Sandra', 'age': 10}, 
        {'name': 'Chris', 'age': 20},
        {'name': 'Andreas', 'age': 35},
        {'name': 'Hong', 'age': 50},
    ])

    df = (CompData(df) >> 
        mutate(birthyear = 2021-df['age']) >>
        filter('age >= 10') >>
        select('name', 'birthyear') >>
        rename({'birthyear': 'birth_year'}) >>
        (lambda x: x['name']) >>
        out()
    )
    print(df)

    mylist = list(range(100))

    summed = (CompData(mylist) >>
        (lambda l: list(map(lambda x: x * 2, l))) >>
        sum >>
        out()
    )
    print(summed)

