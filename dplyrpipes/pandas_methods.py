


###################### dplyr equivalent overloads ####################

@comp_decorator
def filter_df(df, *args, **kwargs):
    return df.query(*args, **kwargs)

@comp_decorator
def select_df(df, *colnames):
    return df[list(colnames)]

@comp_decorator
def arrange_df(df, *colnames, **kwargs):
    return df.sort_values(colnames, **kwargs)

@comp_decorator
def rename_df(df, *args, **kwargs):
    return df.rename(*args, **kwargs)

@comp_decorator
def mutate_df(df, *args, **kwargs):
    return df.assign(*args, **kwargs)

@comp_decorator
def summary_df(df, *args, **kwargs):
    return df.describe(*args, **kwargs)

