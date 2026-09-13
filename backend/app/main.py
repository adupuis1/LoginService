from fastapi import FastAPI
from fastapi.routing import APIRoute 
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.db import create_db_and_tables
from app.api.main import api_router
from app.api.routes import wellknown

def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/api/docs",
    redoc_url=None,
    generate_unique_id_function=custom_generate_unique_id,
)


create_db_and_tables()
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(wellknown.router)

@app.exception_handler(RequestValidationError)
async def validation_handler(request, exc):
    return JSONResponse(status_code=400, content={"detail": exc.errors()})

