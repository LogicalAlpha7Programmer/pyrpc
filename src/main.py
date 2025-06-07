from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from fast_pyrpc import Trpc, schemaW
from fast_pyrpc.fp import flow, pipe
from fast_pyrpc.tuple import TP
app = FastAPI(title="PYRPC", summary="A TRPC Framework built for python", swagger_ui_parameters={"syntaxHighlight.theme": "monokai"})
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
    # api_router=APIRouter(tags=['hello']),
    simple_query=(
        public
        .use(lambda ctx: 5)
        .input(schemaW(P))
        .query(lambda input, ctx: (f"{input.k}:{input.i + ctx}",)[-1])
    ),

    calc_mutation=(
        public
        .use(flow(lambda _: 3, lambda x: x + 7))
        .input(schemaW(P))
        .mutation(lambda input, ctx: (input.i * ctx,)[-1])
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
        )[-1])
    ),

    chained_pipe=(
        public
        .use(flow(lambda _: 1, lambda x: x + 1, lambda x: x * 2))
        .input(schemaW(P))
        .mutation(lambda input, ctx: (
            pipe(input.i, lambda x: x + 1, lambda x: x * ctx),
        )[-1])
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
        )[-1])
    ),
)

# @public.decorator.query
# async def _(input: P, ctx: int = Depends(lambda _: 8)):
#
#     pass
