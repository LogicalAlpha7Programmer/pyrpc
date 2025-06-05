# import inspect
# from typing import Callable
# import asyncio
#
#
# conditional_assignment: Callable[[float], float] = lambda x: (
#     (square := x**2) if x % 2 == 0 else (cube := x**3),  # Conditional assignment
#     square if x % 2 == 0 else cube,
# )[-1]
#
# result = conditional_assignment(3)
# print("Conditional Result:", result)
#
#
# assign_in_tuple: Callable[[float], tuple[float, float]] = lambda x: (
#     (square := x**2),  # Assign square
#     (cube := x**3),  # Assign cube
#     (cube, square),  # Return cube
# )[-1]
#
# result = assign_in_tuple(3)
# print("Result:", result)  # Output: 27
#
# def merge_signatures(sig1: inspect.Signature, sig2: inspect.Signature) -> inspect.Signature:
#     """
#     Merges two function signatures into one.
#     If duplicate parameter names exist, the first signature's parameters take priority.
#     """
#     parameters = {param.name: param for param in sig1.parameters.values()}
#     parameters.update(sig2.parameters)  # Add/Update with second signature's params
#
#     return inspect.Signature(parameters.values())
#
# class MyClass[C]:
#     def __init__(self, **opts: C):
#         self.opts = opts
#
#     def decorator_func(self, **params):
#         def wrapper[A, B](func: Callable[[A], B]):
#
#             async def wrapped(*args, **kwargs):
#                 print("kwargs:", kwargs, "args", args)
#                 return await func(*args, **kwargs, **self.opts, **params)
#             sig = inspect.signature(func)
#             parameters = {param.name: param for param in sig.parameters.values()}
#             self.opts.update(params)
#             parameters.update({"**opts": inspect.Parameter("opts")})
#             return wrapped
#
#         return wrapper
#
#
# c = MyClass(o=2, k=5)
#
#
# @c.decorator_func(x=2, y=5)
# async def hello(c=1, b=2, **opts):
#     print("b:", b, "c:", c, "opts:", opts)
#
#
# asyncio.run(hello(c=2, b=3, m=3))
#
#


pipe = lambda a, fb, *fs: (
    (b := fb(a)) and
    (lambda c=fs, x=b: x if not c else pipe(x, *c))()
)

flow = lambda fb, *fs: lambda a=None: pipe(a, fb, *fs)

# Example usage
result = pipe(3,
              lambda x: x + 2,
              lambda x: x * 3,
              lambda x: x - 1)
print("Pipe Result:", result)  # Output: 14

f = flow(lambda x=None: 1 if x is None else x + 1,
         lambda x: x * 2,
         lambda x: x - 3)

print("Flow Result:", f(5))  # Output: 9
