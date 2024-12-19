from typing import Callable
import asyncio

conditional_assignment: Callable[[float], float] = lambda x: (
    (square := x**2) if x % 2 == 0 else (cube := x**3),  # Conditional assignment
    square if x % 2 == 0 else cube,
)[-1]

result = conditional_assignment(3)
print("Conditional Result:", result)


assign_in_tuple: Callable[[float], tuple[float, float]] = lambda x: (
    (square := x**2),  # Assign square
    (cube := x**3),  # Assign cube
    (cube, square),  # Return cube
)[-1]

result = assign_in_tuple(3)
print("Result:", result)  # Output: 27


class MyClass:
    def __init__(self, **opts):
        self.opts = opts

    def decorator_func(self, x, y):
        def wrapper(func):

            async def wrapped(*args, **kwargs):
                print("kwargs:", kwargs, "args", args)
                return await func(*args, **kwargs, **self.opts, x=x, y=y)

            return wrapped

        return wrapper


c = MyClass(o=2, k=5)


@c.decorator_func(x=2, y=5)
async def hello(c=1, b=2, **opts):
    print("b:", b, "c:", c, "opts:", opts)


asyncio.run(hello(c=2, b=3, m=3))
