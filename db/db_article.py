from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from db.hash import Hash
from db.models import DbArticle
from exception import StoryException

from schemas import ArticleBase

def create_article(db: Session, request: ArticleBase):
    if request.content.startswith('percubaan'):
       raise StoryException('No BM please')
    new_article = DbArticle(
        title = request.title,
        content = request.content,
        published = request.published,
        user_id = request.creator_id )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

def get_article(db: Session, id: int):
    article = db.query(DbArticle).filter(DbArticle.id== id).first()
    if not article:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Article with id {id} not found")
    return article

def update_user(db: Session, id: int, request: ArticleBase):
  article = db.query(DbArticle).filter(DbArticle.id == id)
  if not article.first():
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Article with id {id} not found")
  article.update(
     {
        DbArticle.title: request.title,
        DbArticle.content: request.content,
        DbArticle.published: request.published,
        DbArticle.user_id: request.creator_id
     }
  )
  db.commit()
  return "ok"

def delete_user(db: Session, id: int):
  article = db.query(DbArticle).filter(DbArticle.id == id).first()
  if not article:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Article with id {id} not found")
  db.delete(article)
  db.commit()
  return "ok"