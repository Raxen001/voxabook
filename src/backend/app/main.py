from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.exception import AlreadyExistsError, NotFoundError, UpdateFailedError
from app.routes import api_router


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)


@app.exception_handler(NotFoundError)
def not_found_handler(_request: Request, exception: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exception)})


@app.exception_handler(AlreadyExistsError)
def already_exists_handler(_request: Request, exception: AlreadyExistsError):
    return JSONResponse(status_code=409, content={"detail": str(exception)})


@app.exception_handler(UpdateFailedError)
def update_failed_handler(_request: Request, exception: UpdateFailedError):
    return JSONResponse(status_code=409, content={"detail": str(exception)})


# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
