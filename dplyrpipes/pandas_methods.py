
from .decorators import component

###################### dplyr equivalent overloads ####################

@component
def filter_df(df, *args, **kwargs):
    return df.query(*args, **kwargs)

@component
def select_df(df, *colnames):
    return df[list(colnames)]

@component
def arrange_df(df, *colnames, **kwargs):
    return df.sort_values(colnames, **kwargs)

@component
def rename_df(df, *args, **kwargs):
    return df.rename(*args, **kwargs)

@component
def mutate_df(df, *args, **kwargs):
    return df.assign(*args, **kwargs)

@component
def summary_df(df, *args, **kwargs):
    return df.describe(*args, **kwargs)

