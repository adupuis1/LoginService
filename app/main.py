from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponses

from app.config import settings

app = FastAPI(title=settings.PROJECT_NAME)



@app.exception_handler(RequestValidationError)
async def validation_handler(request, exc):
    return JSONResponses(status_code=400, content={"detail": exc.errors()})

@app.get("/ping")
def ping():
    return {"status":"ok"}