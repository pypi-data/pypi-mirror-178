import fastapi
import mantik.unicore.exceptions as _exceptions
import starlette.status as status


class UnsupportedFileTypeException(fastapi.HTTPException):
    """Authentication has failed."""

    def __init__(
        self,
        detail: str,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            headers=None,
        )


async def unicore_exception_handler(
    request: fastapi.Request, exc: _exceptions.UnicoreError  # noqa
) -> fastapi.responses.JSONResponse:
    return fastapi.responses.JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": f"Unicore backend error. Cause: {str(exc)}"},
    )
