from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.auth import UserSignup, UserLogin, TokenResponse
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService 
from app.database import get_db
from app.utils.exceptions import UserAlreadyExistsError, InvalidCredentialsError, UserNotFoundError 

router = APIRouter()

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup_user(user_in: UserSignup, db: Session = Depends(get_db)):

    auth_service = AuthService(db)
    try:
        user = auth_service.create_user(user_in=user_in)
        return user
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

@router.post("/login", response_model=TokenResponse)
def login_user(user_in: UserLogin, db: Session = Depends(get_db)):

    auth_service = AuthService(db)
    try:
        user = auth_service.authenticate_user(email=user_in.email, password=user_in.password)
        
        dummy_token = f"fake_token_for_user_{user.id}"
        return TokenResponse(
            token=dummy_token,
            token_type="bearer",
            expires_in=3600
        )
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):

    auth_service = AuthService(db)
    try:
        user = auth_service.get_user_by_id(user_id)
        return user
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

@router.get("/users/", response_model=List[UserResponse])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    auth_service = AuthService(db)
    users = auth_service.get_users(skip=skip, limit=limit)
    return users