from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_swagger_ui_html
import sentry_sdk
import redis.asyncio as redis
from database import Base, engine
from routes import user_routes, article_routes
from config import settings
from utils.error_handlers import (custom_http_exception_handler, validation_exception_handler,
                                  authentication_exception_handler)
from sqlalchemy.orm import Session
from models import User as UserModel
from jose import jwt, JWTError
from database import get_db

sentry_sdk.init(
    dsn=settings.sentry_dsn,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dmitriy Belkin Blog - Stage",
    version="0.2.0",
    docs_url="/api/v1/swagger",
    redoc_url="/api/v1/redoc"
)

templates = Jinja2Templates(directory="templates")
app.mount("/articles", StaticFiles(directory="articles"), name="articles")
app.mount("/static", StaticFiles(directory="static"), name="static")

redis_client = redis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)

app.include_router(user_routes.router, prefix="/user", tags=["User"])
app.include_router(article_routes.router, prefix="/articles", tags=["Articles"])

app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, authentication_exception_handler)

@app.get("/api/v1/swagger", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Custom API Docs",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_ui_bundle_url="/static/swagger-ui-standalone-preset.js",
        swagger_favicon_url="/static/favicon.ico",
        swagger_url="/static/swagger.yaml",
        template_name="swagger_ui.html",
    )


def get_authenticated_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if token:
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            username = payload.get("sub")
            if username:
                user = db.query(UserModel).filter(UserModel.username == username).first()
                if user:
                    return user
        except JWTError:
            return None
    return None


@app.get("/", response_class=HTMLResponse, tags=["General"])
async def homepage(request: Request, db: Session = Depends(get_db)):
    user = get_authenticated_user(request, db)
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


@app.get("/login", response_class=HTMLResponse, tags=["Auth"])
async def login_form(request: Request, error: str = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})


@app.get("/register", response_class=HTMLResponse, tags=["Auth"])
async def register_user_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
