from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate 


def create_post_db(db: Session, text: str, author_id: int) -> Post:

    db_post = Post(text=text, author_id=author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts_by_author_db(db: Session, author_id: int) -> List[Post]:

    return db.query(Post).filter(Post.author_id == author_id).order_by(Post.created_at.desc()).all()

def get_post_by_id_and_author_db(db: Session, post_id: int, author_id: int) -> Optional[Post]:

    return db.query(Post).filter(Post.id == post_id, Post.author_id == author_id).first()

def update_post_db(db: Session, db_post: Post, text: Optional[str]) -> Post:

    if text is not None:
        db_post.text = text
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post_db(db: Session, db_post: Post):

    db.delete(db_post)
    db.commit()