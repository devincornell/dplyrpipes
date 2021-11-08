
import functools
import pandas as pd
import functools
import statistics

from dplyrpipes import component, InputData, out
from dplyrpipes import mutate_df, filter_df, rename_df, select_df


if __name__ == '__main__':

    def myfunc1(x, y=1):
        return x * y
    
    result = (InputData(1) >> 
        (lambda x: x + 1) >> 
        myfunc1 >>
        out()
    )
    assert(result == 2)
    print(result)

    result = (InputData(1) >> 
        functools.partial(myfunc1, y=2) >>
        out()
    )
    assert(result == 2)
    print(result)

    @component
    def myfunc2(x, y, z=1):
        return x * y * z

    result = (InputData(1) >> 
        (lambda x: x + 1) >> 
        myfunc2(3, z=2) >>
        out()
    )
    assert(result == 12)
    print(result)
    
    mylist = list(range(3))
    result = (InputData(mylist) >> 
        (lambda l: l + [4]) >> 
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
    

