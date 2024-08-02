from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_404_NOT_FOUND
from jose import jwt, JWTError
from datetime import timedelta
from sqlalchemy.orm import Session
import markdown
import json
from redis_client import get_redis, close_redis
from database import SessionLocal, engine, Base
from models import User, Article
from auth import authenticate_user, create_access_token, get_password_hash, get_current_active_user
from schemas import Token, User as UserSchema
from config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Подключение шаблонов и статических файлов
templates = Jinja2Templates(directory="templates")
app.mount("/articles", StaticFiles(directory="articles"), name="articles")
app.mount("/static", StaticFiles(directory="static"), name="static")


# Добавление обработчика ошибок
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == HTTP_404_NOT_FOUND:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=exc.status_code)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": exc.errors(), "body": exc.body})


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_authenticated_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if token:
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            username = payload.get("sub")
            if username:
                user = db.query(User).filter(User.username == username).first()
                if user:
                    return user
        except JWTError:
            return None
    return None


@app.on_event("startup")
async def startup():
    await get_redis()


@app.on_event("shutdown")
async def shutdown():
    await close_redis()


@app.post("/token", response_model=Token, tags=["Auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return RedirectResponse(url="/login?error=incorrect_credentials", status_code=status.HTTP_302_FOUND)
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response


@app.post("/register", response_model=UserSchema)
def register_user(username: str = Form(...), password: str = Form(...), email: str = Form(...),
                  full_name: str = Form(...), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(password)
    new_user = User(username=username, full_name=full_name, email=email, hashed_password=hashed_password,
                    is_active=True)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/upload", tags=["Articles"])
async def upload_article(title: str = Form(...), file: UploadFile = File(...),
                         current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """
    Upload a new markdown article.
    """
    if file.content_type != "text/markdown":
        raise HTTPException(status_code=400, detail="Invalid file type")

    content = await file.read()
    new_article = Article(
        title=title,
        content=content.decode("utf-8"),
        owner_id=current_user.id
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)

    return {"title": title}


@app.get("/articles/{article_id}", response_class=HTMLResponse, tags=["Articles"])
async def read_article(request: Request, article_id: int, db: Session = Depends(get_db)):
    """
    Read a specific article by ID.
    """
    user = get_authenticated_user(request, db)
    if user is None:
        return RedirectResponse(url="/login")

    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    html_content = markdown.markdown(article.content)
    return templates.TemplateResponse("article.html", {"request": request, "article": article, "content": html_content})


@app.get("/articles", tags=["Articles"])
async def list_articles(db: Session = Depends(get_db)):
    """
    List all articles.
    """
    redis = await get_redis()
    cached_articles = await redis.get("articles")
    if cached_articles:
        articles = json.loads(cached_articles)
        return articles

    articles = db.query(Article).all()
    articles_data = [article.as_dict() for article in articles]
    await redis.set("articles", json.dumps(articles_data))
    return articles


@app.get("/login", response_class=HTMLResponse, tags=["Auth"])
async def login_form(request: Request, error: str = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})


@app.get("/register", response_class=HTMLResponse, tags=["Auth"])
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/", response_class=HTMLResponse, tags=["General"])
async def homepage(request: Request):
    user = get_authenticated_user(request)
    return templates.TemplateResponse("index.html", {"request": request, "user": user})
