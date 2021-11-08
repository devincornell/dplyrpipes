# `dplyrpipes` Package

This package was built to emulate the behavior of dplyr by adding some syntactic sugar. I essentially created an interface that uses the `>>` operator instead of dplyr's `%>%` operator to pass data through functions. I personally don't run into situations where this syntax is helpful, but I thought I'd make it just to show it can be done. Maybe someone will find it helpful 🤷.

Two language differences were important to consider when writing this package: (1) Python does not allow us to create new global operators - only define operator behavior relative to a given class; and (2) function calls cannot include variables that are not in-scope (like we see dplyr use in mutate or select functions), so they typically must be provided as strings.

My solution requires you to pass your input data to the `InputData` constructor which overloads the `>>` operator, so that, evaluated left-to-right, it will repeatedly apply functions on the right-hand side until it encounters `out()` object that will actually return your data.

This example shows how you can pass regular functions (including lambdas) to be applied to the input. I wrapped the expression in parentheses to look more like `dplyr` conventions.

```
def myfunc1(x, y=1):
    return x * y

result = (InputData(1) >> 
    (lambda x: x + 1) >> 
    myfunc1 >>
    out()
)
# result == 2
```

You can also use `functools.partial` to pass builtin functions with arguments, or even directly pass functions that require only the input as an argument.

```
result = (InputData(1) >> 
    functools.partial(myfunc1, y=2) >>
    out()
)
# result == 2
```

You can also use the `@component` decorator to wrap your function defintion so you don't need `functools.partial`. This allows you to pass functions that look like function calls with the expected parameters. In this example, see how a call to `myfunc2`, wrapped using the `@component` decorator, returns a function that accepts one argument and passes all other args and keyword arguments to the other parameters.

```
@component
def myfunc2(x, y, z=1):
    return x * y * z

result = (InputData(1) >> 
    myfunc2(3, z=2) >>
    out()
)
# result == 12
```


Now for dataframe manipulation. In `dplyr` many operations such as `mutate()` and `select()` look like function calls, but are applied to the intput as if they were functions, so I created a few mappings from equivalent pandas and 

```
# example dataframe
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
```

Obviously I didn't bother to translate all pandas to dplyr methods, but you can use a [translation guide like this one](https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_r.html) to write your own translations if you want.

