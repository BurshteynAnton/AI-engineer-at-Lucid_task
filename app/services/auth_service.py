from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.crud import user as user_crud
from app.core.security import get_password_hash, verify_password
from app.utils.exceptions import UserAlreadyExistsError, InvalidCredentialsError, UserNotFoundError


class AuthService:

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_in: UserCreate) -> User:

        existing_user = user_crud.get_user_by_email_db(self.db, user_in.email)
        if existing_user:
            raise UserAlreadyExistsError(user_in.email)
            
        hashed_password = get_password_hash(user_in.password)
        db_user = user_crud.create_user_db(self.db, user_in.email, hashed_password)
        return db_user

    def authenticate_user(self, email: str, password: str) -> User:

        user = user_crud.get_user_by_email_db(self.db, email)
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError
        return user

    def get_user_by_id(self, user_id: int) -> User:

        user = user_crud.get_user_by_id_db(self.db, user_id)
        if not user:
            raise UserNotFoundError(user_id=user_id)
        return user

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:

        return user_crud.get_users_db(self.db, skip=skip, limit=limit)