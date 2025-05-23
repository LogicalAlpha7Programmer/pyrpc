from fastapi import FastAPI
from src.core import Trpc, schemaW
from pydantic import BaseModel, Field

app = FastAPI(
    swagger_ui_parameters={
        "syntaxHighlight.theme": "monokai"
    }
)
trpc = Trpc(app)


class P(BaseModel):
    i: int
    k: str = Field(default="sdt")


public_procedure = trpc.procedure

k = trpc.router("Hello",
    a={
        "b": public_procedure.use(lambda ctx: 4)
        .input(schemaW(P))
        .query(lambda input, ctx: f"{input.k}: {input.i + ctx}")
    },
    b=trpc.procedure.use(lambda ctx: 4)
    .input(schemaW(P))
    .mutation(lambda input, ctx: input.i + ctx),
)


