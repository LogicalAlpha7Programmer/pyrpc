from fp_py import pipe
from fastapi import FastAPI, Depends, APIRouter
from core import Trpc, schemaW
from pydantic import BaseModel, Field

app = FastAPI()
trpc = Trpc(app)


class P(BaseModel):
    i: int
    k: str = Field(default="")


k = trpc.router(
    a={
        "b": trpc.procedure()
        .use(lambda ctx: 4)
        .input(schemaW(P))
        .query(lambda input, ctx: f"{input.k}: {input.i + ctx}")
    },
    b=trpc.procedure()
    .use(lambda ctx: 4)
    .input(schemaW(P))
    .mutation(lambda input, ctx: input.i + ctx),
)
m = k["a.b"](i=6, k="hello")