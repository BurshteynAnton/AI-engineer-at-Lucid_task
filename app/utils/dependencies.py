from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import AuthService 
from app.models.user import User
from app.utils.exceptions import UserNotFoundError 

class CurrentUserStub:

    def __call__(self, db: Session = Depends(get_db)):
        auth_service = AuthService(db)
        try:
           
            user = auth_service.get_user_by_id(1) 
            return user
        except UserNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated or default user (ID 1) not found. Please create a user via signup.",
                headers={"WWW-Authenticate": "Bearer"},
            )

get_current_user = CurrentUserStub() 