from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import markdown
from database import get_db
from models import Article, User as UserModel
from auth import get_current_active_user

router = APIRouter()


@router.post("/upload", tags=["Articles"])
async def upload_article(title: str = Form(...), file: UploadFile = File(...),
                         current_user: UserModel = Depends(get_current_active_user), db: Session = Depends(get_db)):
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


@router.get("/{article_id}", tags=["Articles"])
async def read_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    html_content = markdown.markdown(article.content)
    return {"title": article.title, "content": html_content}


@router.get("/", tags=["Articles"])
async def list_articles(db: Session = Depends(get_db)):
    articles = db.query(Article).all()
    return articles
