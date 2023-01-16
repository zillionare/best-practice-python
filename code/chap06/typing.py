
from typing import Any
import cfg4py

s = 1         # Statically typed (type int)
reveal_type(s)
d: Any = 1    # Dynamically typed (type Any)
reveal_type(d)
s = 'x'       # Type check error
d = 'x'       # OK

def foo(name: str)->int:
    score = 20
    return score

# print(foo(10))

def bar(name):
    x = 1
    reveal_type(x)
    x.foo()
    return name

bar("aaron")

def bar2()->None:
    not_very_wise = "1" + 1
