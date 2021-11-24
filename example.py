
import functools
import pandas as pd
import functools
import statistics

from dplyrpipes import component, PipeData, out
from dplyrpipes import mutate_df, filter_df, rename_df, select_df


if __name__ == '__main__':

    def myfunc1(x, y=1):
        return x * y
    
    result = (PipeData(1) >> 
        (lambda x: x + 1) >> 
        myfunc1 >>
        out()
    )
    assert(result == 2)
    print(result)

    result = (PipeData(1) >> 
        functools.partial(myfunc1, y=2) >>
        out()
    )
    assert(result == 2)
    print(result)

    @component
    def myfunc2(x, y, z=1):
        return x * y * z

    result = (PipeData(1) >> 
        (lambda x: x + 1) >> 
        myfunc2(3, z=2) >>
        out()
    )
    assert(result == 12)
    print(result)
    
    mylist = list(range(3))
    result = (PipeData(mylist) >> 
        (lambda l: l + [4]) >> 
        sum >>
        out()
    )
    print(result)
    
    example_df = pd.DataFrame([
        {'name': 'Karl', 'age': 7, 'gender': 'none'}, 
        {'name': 'Sandra', 'age': 10, 'gender': 'male'}, 
        {'name': 'Chris', 'age': 20, 'gender': 'female'},
        {'name': 'Andreas', 'age': 35, 'gender': 'none'},
        {'name': 'Hong', 'age': 50, 'gender': 'female'},
    ])

    # this shows some built-in methods that emulate behavior of dplyr methods
    df = (PipeData(example_df) >> 
        mutate_df(birthyear = 2021-example_df['age']) >>
        filter_df('age >= 10') >>
        select_df('name', 'birthyear') >>
        rename_df({'birthyear': 'birth_year'}) >>
        out()
    )
    print(df)

    # and another example implementing a pandas method
    @component
    def count(df, *args, **kwargs):
        return df.groupby(*args, **kwargs).size()

    df = (PipeData(example_df) >>
        count('gender') >>
        out()
    )
    print(df)
    

