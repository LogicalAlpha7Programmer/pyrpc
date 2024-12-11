from re import error
from typing import Optional
from fp_py import pipe
from fastapi import FastAPI, Depends, APIRouter
from core import Procedure, Trpc, ExecuteTypes
from core import ClassType, schemaW, typeof, Procedure, dot_shrink, map_routes
from pydantic import BaseModel, Field

app = FastAPI()
trpc = Trpc(app)


# def get_path_call(path: str, trpc: Trpc, execution_type: int):
#     try:
#         trpc_execute = trpc.routes[path]
#         if execution_type == trpc_execute.__execute_type__:
#             return trpc_execute()
#     except Exception:
#         raise error("no such path for this execution_type found")
#
#
class P(BaseModel):
    i: int
    k: str = Field(default="")


#
#
# base = trpc.procedure()
# auth = base.use(lambda _: 20)
# protected = auth.use(lambda ctx: pipe(20, lambda a: ctx == a))
# # Add an input schema for the execute function
# signIn = protected.input(schemaW(P)).query(
#     lambda input, ctx: f"succeshh {ctx} {input.i}"
# )
# trpc.router("hello", a={"b": signIn})
#
#
# @app.post(path="/{path}")
# def mutation(path: str):
#     print(trpc.routes)
#     return get_path_call(path, trpc, ExecuteTypes.MUTATION)
#
#
# @app.get(path="/{path}")
# def query(path: str):
#     return get_path_call(path, trpc, ExecuteTypes.QUERY)
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
# search_params = "?auth.sign_in&data=''"
#
# get_path(searchParams) # auth.sign_in as string
# path = 'auth.sign_in'
#
# get_dict_path(paht) # ['auth', 'sign_in']
# dict_path = ['auth', 'sign_in']
#
# get_procedure_from_dict_path(dict_path) # procedure
# procedure = app_router.auth.sign_in
#
# get_params_from_search_query(search_params)
# params = { }
#
# resutl = procedure.mutate(params)
#
# return result

# https://someapi.com/api/trpc


# req = requests.request("GET", f"www.google.com?q='{P}")
