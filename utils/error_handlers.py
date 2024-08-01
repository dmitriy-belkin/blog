from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError  # Добавлен импорт RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_404_NOT_FOUND

templates = Jinja2Templates(directory="templates")


async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == HTTP_404_NOT_FOUND:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=exc.status_code)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    body_content = exc.body.decode('utf-8') if isinstance(exc.body, bytes) else exc.body
    return JSONResponse(
        status_code=400,
        content={
            "detail": exc.errors(),
            "body": body_content
        }
    )


async def authentication_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
