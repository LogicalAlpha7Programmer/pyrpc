from fastapi import Depends
from pydantic import BaseModel
from core import ClassType, schemaW, typeof, Procedure, dot_shrink
from json_obj import obj
from fp_py import pipe
from typing import TypedDict, Callable
from dataclasses import dataclass

# Example usage
example = obj(x=1, k="3")
for key, value in example:
    print(f"{key}: {value}")
print(example)


class Router(obj):
    pass


class P(BaseModel):
    i: int


class M(BaseModel):
    m: int


base = Procedure()
auth = base.use(lambda _: 20)
protected = auth.use(lambda ctx: pipe(20, lambda a: ctx == a))
# Add an input schema for the execute function
signIn = protected.input(schemaW(P)).query(
    lambda input, ctx: f"succeshh {ctx} {input.i}"
)

# Call execute function with the input

router = obj(
    auth=obj(
        sign_in=signIn,
        sign_up=auth.input(schemaW(M)).mutation(lambda inputs, ctx: "23"),
    ),
    h=signIn,
)

router.k = base.input(schemaW(M)).mutation(lambda input, ctx: "")

k = router.auth.sign_in(P(i=2))
s = {"a": 3, "b": {"c": {"d": 1}}, "e": {"f": 4}}
print(dot_shrink(s))
print(k)
print(type({"a": {}}))
