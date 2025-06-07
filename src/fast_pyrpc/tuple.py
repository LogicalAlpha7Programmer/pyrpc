from typing import Callable
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

class Statement:
    pass

class tif[A, D](Statement):
    def __init__(self, condition: bool, value: A = None, alternate: D = None) -> None:
        self.condition = condition
        self.value = value
        self.alternate = alternate

    def then[B](self, value: B):
        if self.condition:
            return tif(self.condition, value, self.alternate)
        return self

    def else_if(self, condition: bool):
        return tif(condition)

    def else_then[C](self, value: C):
        t_if = self if self.condition else tif(self.condition, value ,self.value)
        # relse_eturn t_if.value if t_if.value is not None else t_if.alternate
        return t_if
    @property
    def result(self):
        t_if = self.else_then(None)
        return t_if.value if t_if.value is not None else t_if.alternate



class Case[CV, MB, CR](Statement):
    def __init__(self, value: CV, matched: MB = False, result: CR = None ) -> None:
        self.value = value
        self.matched = matched
        self.result = result

    def case[CB](self, condition: Callable[[CV], CB]):
        if not self.matched and condition(self.value):
            return Case(self.value, condition(self.value), self.result)
        return self

    def then[CT](self, result: CT):
        if self.matched and self.result is None:
            return Case(self.value, self.matched, result)
        return self

    def default[DR](self, result: DR):
        return self if self.result is not None else Case(self.value, self.matched, result)


class For[A, C, R](Statement):
    def __init__(self, initializer: A, condition: Callable[[A], bool], operation: Callable[[A], C], _result: Callable[[A, Callable[[A], bool], Callable[[A], C]], R]) -> None:
        self.initializer = initializer
        self.condition = condition
        self.operation = operation
        self._result = _result

    def then[Rn](self, result: Callable[[A, Callable[[A], bool], Callable[[A], C]], Rn]):
        return For(self.initializer, self.condition, self.operation, result)
    
    @property
    def result(self):
        i = self.initializer
        k = None
        while self.condition(i):
            k = self._result(i, self.condition, self.operation(i))
            i = self.operation(i)
        return k

class TP:
    def __init__(self) -> None:
        self.If = tif
        self.Match = Case

tp = TP()
# Usage Example
result: Callable[[int], int | str | None] = lambda y: (
    tp.If(y > 2)
    .then(((x := 3),x + y)[-1])
    .else_then(((x := x + 6),"False Case " + str(x))[-1])
    .result
)

print("Chained Result:", result(3))  # Output: "True Case"

# Chained example
result2 = tp.If(3 < 2 and 4 < 2).then("True Case").else_if(9 < 5).then("Else-If Case").result
print("Chained Result with Else-If:", result2)  # Output: "Else-If Case"



# Example Usage:
x = 10

result3 = (tp.Match(x)
          .case(lambda m: m == 1).then(1)
          .case(lambda x: x == 2).then("Two")
          .case(lambda x: x == 3).then("Three")
          .default("Other").result)


print("Case Result:", (1, 2, 4)*2)  # Output: "Three"

