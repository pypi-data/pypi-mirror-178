# `pycodemarker`

The `pycodemarker` is a simple tool that can be used to instrument your downstream HTTP API calls and your internal functions. Their behavior can then be visualised in Doctor Droid's platform. Visit - https://drdroid.io

`from pycodemarker import codemarker`

`@codemarker.droid_peek
def func(arg1, arg2):
    return arg1 + arg2
`

