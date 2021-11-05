
from typing import Callable, Any, Union, List
import functools

import dataclasses

import pandas as pd


if __name__ == '__main__':
    
    df = pd.DataFrame([
        {'name': 'Karl', 'age': 7}, 
        {'name': 'Sandra', 'age': 10}, 
        {'name': 'Chris', 'age': 20},
        {'name': 'Andreas', 'age': 35},
        {'name': 'Hong', 'age': 50},
    ])

    df = (CompData(df) >> 
        mutate_df(birthyear = 2021-df['age']) >>
        filter('age >= 10') >>
        select_df('name', 'birthyear') >>
        rename_df({'birthyear': 'birth_year'}) >>
        component((lambda df,y: df['birth_year'] + 1 + y))(2) >>
        out()
    )
    print(df)

    import functools
    import statistics
    mylist = list(range(100))
    summed = (CompData(mylist) >>
        (lambda l: list(map(lambda x: x * 2, l))) >>
        functools.partial(sorted, reverse=True) >>
        functools.partial(itertools.filter)
        statistics.median 
    ) >> out()
    print(summed)

