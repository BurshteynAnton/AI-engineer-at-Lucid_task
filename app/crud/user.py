from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.user import User
from app.schemas.user import UserCreate 


def get_user_by_email_db(db: Session, email: str) -> Optional[User]:

    return db.query(User).filter(User.email == email).first()

def create_user_db(db: Session, email: str, password_hash: str) -> User:

    db_user = User(email=email, password_hash=password_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id_db(db: Session, user_id: int) -> Optional[User]:

    return db.query(User).filter(User.id == user_id).first()

def get_users_db(db: Session, skip: int = 0, limit: int = 100) -> List[User]:

    return db.query(User).offset(skip).limit(limit).all()
