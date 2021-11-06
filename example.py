
import functools
import pandas as pd
import functools
import statistics

from dplyrpipes import InputData, mutate_df, filter_df, rename_df, select_df, out

if __name__ == '__main__':

    result = (InputData(1) >> 
        (lambda x: x + 1) >> 
        out()
    )
    print(result)

    mylist = list(range(3))
    result = (InputData(mylist) >> 
        (lambda l: l + [4]) >> 
        functools.partial(filter, lambda x: x >= 2) >>
        sum >>
        out()
    )
    print(result)
    
    example_df = pd.DataFrame([
        {'name': 'Karl', 'age': 7}, 
        {'name': 'Sandra', 'age': 10}, 
        {'name': 'Chris', 'age': 20},
        {'name': 'Andreas', 'age': 35},
        {'name': 'Hong', 'age': 50},
    ])

    # this shows some built-in methods that emulate behavior of dplyr methods
    df = (InputData(example_df) >> 
        mutate_df(birthyear = 2021-example_df['age']) >>
        filter_df('age >= 10') >>
        select_df('name', 'birthyear') >>
        rename_df({'birthyear': 'birth_year'}) >>
        out()
    )
    print(df)

    # this shows the pipes applied to normal functions
    mylist = list(range(100))
    summed = (InputData(mylist) >>
        (lambda l: list(map(lambda x: x * 2, l))) >>
        functools.partial(sorted, reverse=True) >>
        functools.partial(filter, lambda x: x > 10) >>
        statistics.median >>
        out()
    )
    print(summed)

