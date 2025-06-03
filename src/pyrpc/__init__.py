
from enum import Enum
import inspect
from typing import Callable, Any

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, create_model
from . import fp

# Define type variables
class ClassType[C]:
    type: C = NotImplemented


class ExecuteTypes:
    MUTATION = 1
    QUERY = 2


def typeof(obj):
    return ClassType[obj].type


def schemaW(obj):
    return (obj, ClassType[obj].type)


class ProcedureError(Exception):
    pass


def create_dynamic_model(name: str, schema_dict: dict):
    """
    Creates a dynamic Pydantic model from a dictionary schema.
    """
    return create_model(
        name, **{key: (type(value), value) for key, value in schema_dict.items()}
    )


class Procedure[If, I, C]:
    """
    A Procedure class that handles pipelining middlewares and executing in
    two types of methods: mutate or query
    """

    def __init__(
        self,
        schema_input: If | None = None,
        schema_input_type: I | None = None,
        middlewares_flow: Callable[[Any], C | Any] = lambda x: x,
        wrapped_middleware_func: Callable[
            [Callable[[], C | Any]], C | Any
        ] = lambda x: x(),
    ) -> None:
        """
        An initializer for Procedure
        """
        self.schema_input = schema_input
        self.schema_input_type = schema_input_type
        self.middlewares_flow = middlewares_flow
        self.wrapped_middleware_func = wrapped_middleware_func

    def _get_middleware_context(self):
        """Gets the middlware context"""
        return self.middlewares_flow(None)

    def _get_context(self):
        """Gets the context"""
        return self.wrapped_middleware_func(self._get_middleware_context)

    def input[Ifn, In](self, schemaW: tuple[Ifn, In] | None = None):
        """
        Creates a handler for input schema
        """
        schema_input, schema_input_type = schemaW or (None, None)

        return Procedure[Ifn, In, C](
            schema_input,
            schema_input_type,
            self.middlewares_flow,
            self.wrapped_middleware_func,
        )

    def use[Cf](self, func: Callable[[C], Cf]):
        """
        Adds a middleware function and returns a new Procedure
        with updated middleware input and output types.
        """
        return Procedure[If, I, Cf](
            self.schema_input,
            self.schema_input_type,
            fp.flow(self.middlewares_flow, func),
            self.wrapped_middleware_func,
        )

    def mutation[O](self, func: Callable[[I, C], O]):

        def process_mutation(input: I) -> O:
            """
            Processes the input through all middleware and returns the final mutation output.
            """

            try:
                context: C = self._get_context()
                return func(
                    input, context
                )  # Pass the processed value through the mutation function

            except ProcedureError:
                pass

        process_mutation.__execute_type__ = ExecuteTypes.MUTATION
        process_mutation.__annotations__["input"] = self.schema_input
        return process_mutation

    def query[O](self, func: Callable[[I, C], O]):
        def process_query(**kwargs: ...) -> O:
            """
            Processes the input through all middleware and returns the final query output.
            """
            try:
                context: C = self._get_context()
                return func(
                    self.schema_input(**kwargs), context
                )  # Pass the processed value through the mutation function

            except ProcedureError:
                pass

        process_query.__execute_type__ = ExecuteTypes.QUERY
        process_query.__input_schema__ = self.schema_input
        if issubclass(self.schema_input, BaseModel):
            print(self.schema_input.__signature__)
            process_query.__signature__ = inspect.Signature(
                [
                    inspect.Parameter(
                        key,
                        inspect.Parameter.POSITIONAL_OR_KEYWORD,
                        annotation=value.annotation,
                        default=value.default,
                    )
                    for key, value in self.schema_input.model_fields.items()
                ]
            )
        return process_query



class Trpc:
    def __init__(self, app_or_router: FastAPI | APIRouter) -> None:
        self.procedure = Procedure()
        self.routes: dict[str, Any] = {}
        self.app_or_router = app_or_router
    

    def router(self, router_name: str | None = None, **kwargs):
        """Adds Routes to Trpc"""
        sub_router = APIRouter(tags=[router_name])
        obj = kwargs
        if router_name is not None and not router_name.isspace():
            obj = {router_name: obj}
        routes = map_routes(sub_router, dot_shrink(obj))

        self.routes.update(routes)
        self.app_or_router.include_router(sub_router)
        return routes


def match_procedure_routes[O](router: APIRouter, func: Callable[..., O], path: str):

    match (func.__execute_type__):
        case ExecuteTypes.MUTATION:
            router.add_api_route(f"/{path}", func, methods=["POST"])
        case ExecuteTypes.QUERY:
            router.add_api_route(f"/{path}", func, methods=["GET"])

    return path


def dot_shrink(obj: dict[str, Any]):

    new_obj: dict[str, Any] = {}
    for key in obj:
        if isinstance(obj[key], dict):
            other_obj = dot_shrink(obj[key])
            for other_key in other_obj:
                new_obj[f"{key}.{other_key}"] = other_obj[other_key]
            continue
        new_obj[key] = obj[key]

    return new_obj


def map_routes(router: APIRouter, paths: dict[str, Any]):
    for key in paths:
        match_procedure_routes(router, paths[key], key)

    return paths
