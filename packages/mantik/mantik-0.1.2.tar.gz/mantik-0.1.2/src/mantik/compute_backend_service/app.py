import fastapi
import mantik.compute_backend_service.api as api
import mantik.compute_backend_service.exceptions as exceptions
import mantik.unicore.exceptions as unicore_exceptions


def create_app(
    docs_url: str, redoc_url: str, openapi_url: str, global_path_prefix: str
) -> fastapi.FastAPI:
    app = fastapi.FastAPI(
        docs_url=global_path_prefix + docs_url,
        redoc_url=global_path_prefix + redoc_url,
        openapi_url=global_path_prefix + openapi_url,
    )
    app.include_router(api.router, prefix=global_path_prefix)
    app.add_exception_handler(
        unicore_exceptions.UnicoreError, exceptions.unicore_exception_handler
    )
    return app
