# PyRPC — Python RPC Framework with Tuple Programming

PyRPC is a lightweight Python RPC framework built on FastAPI and Pydantic. It leverages advanced tuple programming, pipeline flow utilities, and type-safe procedures for building scalable RPC endpoints with middleware support.

---

## Features

- **Procedure-based RPC:** Define queries and mutations with input schemas and context-aware middleware.
- **Tuple Programming Style:** Uses tuple expressions for concise conditional logic and assignments.
- **Pipeline Utilities:** Powerful `pipe` and `flow` functions for composing middleware transformations.
- **Dynamic Routing:** Easily organize RPC routes with nested routers and dot notation.
- **Type Safety:** Integrates Pydantic for validation and type enforcement.

---

## Installation

```bash
pip install -i https://test.pypi.org/simple/ pyrpc==0.0.1
or
git clone https://github.com/LogicalAlpha7Programmer/pyrpc.git
```

Clone this repository and include it in your Python path to import `Trpc`, `schemaW`, and related utilities.

---

## Quickstart

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field
from pyrpc import Trpc, schemaW
from pyrpc.tuple import TP
from pyrpc.fp import flow, pipe

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "monokai"})
trpc = Trpc(app)
tp = TP()

class P(BaseModel):
    i: int
    k: str = Field(default="hello")

class Q(BaseModel):
    n: float
    b: bool = Field(default=True)

public = trpc.procedure

router = trpc.router("examples",
    simple_query=(
        public
        .use(lambda ctx: 5)
        .input(schemaW(P))
        .query(lambda input, ctx: (f"{input.k}:{input.i + ctx}",)[0])
    ),

    calc_mutation=(
        public
        .use(flow(lambda _: 3, lambda x: x + 7))
        .input(schemaW(P))
        .mutation(lambda input, ctx: (input.i * ctx,)[0])
    ),

    complex_case=(
        public
        .use(lambda ctx: 10)
        .input(schemaW(Q))
        .query(lambda input, ctx: (
            tp.Match(input.n)
            .case(lambda x: x < 5).then("Small")
            .case(lambda x: 5 <= x <= 10).then("Medium")
            .default("Large")
            .result,
        )[0])
    ),

    chained_pipe=(
        public
        .use(flow(lambda _: 1, lambda x: x + 1, lambda x: x * 2))
        .input(schemaW(P))
        .mutation(lambda input, ctx: (
            pipe(input.i, lambda x: x + 1, lambda x: x * ctx),
        )[0])
    ),

    conditional=(
        public
        .use(lambda ctx: 8)
        .input(schemaW(P))
        .query(lambda input, ctx: (
            tp.If(input.i % 2 == 0)
            .then(f"Even: {input.i + ctx}")
            .else_then(f"Odd: {input.i - ctx}")
            .result,
        )[0])
    ),
)
```

---

## Tuple Programming Utilities

### Pipe and Flow

- `pipe(value, fn1, fn2, ...)`
  Sequentially applies functions to a value, returning the final output.

- `flow(fn1, fn2, ...)`
  Returns a function that takes an initial value and applies a pipeline of functions.

Example:

```python
pipe_result = pipe(3, lambda x: x+1, lambda x: x*2)  # 8
flow_fn = flow(lambda x: x+1, lambda x: x*2)
flow_result = flow_fn(3)  # 8
```

### Conditional (`tp.If`) and Match (`tp.Match`)

- `tp.If(condition).then(value).else_then(other_value).result`
  Chained conditional expression.

- `tp.Match(value).case(predicate).then(result).default(default_result).result`
  Pattern matching with cases.

Example:

```python
cond_result = tp.If(4 > 2).then("Yes").else_then("No").result  # "Yes"

match_result = (
    tp.Match(5)
    .case(lambda x: x < 3).then("Low")
    .case(lambda x: x < 10).then("Mid")
    .default("High")
    .result  # "Mid"
)
```

---

## Middleware Composition

Middleware can be pipelined elegantly using `flow` and combined with `pipe` in mutation/query resolvers:

```python
public.use(flow(lambda _: 1, lambda x: x+2, lambda x: x*3))
```

This pipelines three middleware transformations that ultimately provide a context value used by the procedure.

---

## Why PyRPC?

- Emphasizes immutability and functional composition using tuple syntax.
- Clean separation of concerns with schema validation and middleware.
- Intuitive API design blending FastAPI’s routing with functional programming patterns.

---

## Run the Server

```bash
uvicorn main:app --reload
or
fastapi dev
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API docs with custom Monokai syntax highlighting.

---

_Built with ❤️ and tuples_
_Contributions welcome!_
