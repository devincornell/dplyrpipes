
import functools
import pandas as pd
import functools
import itertools
import statistics

import dplyrpipes

if __name__ == '__main__':
    
    example_df = pd.DataFrame([
        {'name': 'Karl', 'age': 7}, 
        {'name': 'Sandra', 'age': 10}, 
        {'name': 'Chris', 'age': 20},
        {'name': 'Andreas', 'age': 35},
        {'name': 'Hong', 'age': 50},
    ])

    df = (dplyrpipes.InputData(example_df) >> 
        dplyrpipes.mutate_df(birthyear = 2021-example_df['age']) >>
        dplyrpipes.filter_df('age >= 10') >>
        dplyrpipes.select_df('name', 'birthyear') >>
        dplyrpipes.rename_df({'birthyear': 'birth_year'}) >>
        dplyrpipes.component((lambda df,y: df['birth_year'] + 1 + y))(2) >>
        dplyrpipes.out()
    )
    print(df)

    
    mylist = list(range(100))
    summed = (dplyrpipes.InputData(mylist) >>
        (lambda l: list(map(lambda x: x * 2, l))) >>
        functools.partial(sorted, reverse=True) >>
        functools.partial(itertools.filter) >>
        statistics.median >>
        dplyrpipes.out()
    )
    print(summed)

