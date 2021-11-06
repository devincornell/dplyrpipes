# `dplyrpipes` Package

This package was built to emulate the behavior of dplyr by adding some syntactic sugar. I essentially created an interface that uses the `>>` operator instead of dplyr's `%>%` operator to pass data through functions. I personally don't run into situations where this syntax is helpful, but I thought I'd make it just to show it can be done. Maybe someone will find it helpful 🤷.

Two language differences were important to consider when writing this package: (1) Python does not allow us to create new global operators - only define operator behavior relative to a given class; and (2) function calls cannot include variables that are not in-scope (like we see dplyr use in mutate or select functions), so they typically must be provided as strings.

My solution requires you to pass your input data to the `InputData` constructor which overloads the `>>` operator, so that, evaluated left-to-right, it will repeatedly apply functions on the right-hand side until it encounters `out()` object that will actually return your data.

This example shows how you can pass a lambda function to modify the original data by adding one. I wrapped the expression in parentheses to look more like `dplyr` conventions.
```
result = (InputData(1) >> 
    (lambda x: x + 1) >> 
    out()
)
# now result == 2
```

You can also use `functools.partial` to pass builtin functions with arguments, or even directly pass functions that require only the input as an argument.

```
mylist = list(range(3))
result = (InputData(mylist) >> 
    (lambda l: l + [4]) >> 
    functools.partial(filter, lambda x: x >= 2) >>
    sum >>
    out()
)
```


Now for dataframe manipulation. In `dplyr` many operations such as `mutate()` and `select()` look like regular functions, so I created the `@component` decorator to convert your custom functions into ones that return another function that accepts a single argument for the input data and other arguments to be passed when calling that function. It works very similar to For, example, observe the following function definition using the `@component` decorator:
```
@dplyrpipes.component
def mymethod(x, y, z=1):
    return x * y + z
```

In the modified function, the call `mymethod(10, z=2)` will return a function that looks like `newmethod(x, 10, z=2)`.

I created the `@component` decorator to modify user functions to return a new new function which takes the first argument to be passed to the data and remaining.

My solution requres wrapping your input data in the `InputData` class and using `>>` to pipe data 

