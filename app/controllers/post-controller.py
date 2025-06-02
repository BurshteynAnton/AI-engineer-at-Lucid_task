from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.post import PostCreate, PostResponse, PostCreateResponse, PostListResponse, PostDeleteResponse, PostUpdate
from app.services.post_service import PostService 
from app.db.session import get_db
from app.core.security import get_password_hash
from app.models.user import User 
from app.utils.exceptions import PostNotFoundError 
from app.utils.dependencies import get_current_user 


router = APIRouter()

@router.post("/posts", response_model=PostCreateResponse, status_code=status.HTTP_201_CREATED)
def create_new_post(
    post_in: PostCreate,
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):

    post_service = PostService(db)
    db_post = post_service.create_post(post_in=post_in, author_id=current_user.id)
    return PostCreateResponse(postID=db_post.id)


@router.get("/posts", response_model=PostListResponse)
def get_posts_for_user(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):

    post_service = PostService(db)
    user_posts = post_service.get_posts_by_author(author_id=current_user.id)
    
    response_posts = [PostResponse.model_validate(p) for p in user_posts]
    
    return PostListResponse(posts=response_posts, total=len(response_posts), cached=False)


@router.get("/posts/{post_id}", response_model=PostResponse)
def get_single_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    post_service = PostService(db)
    try:
        db_post = post_service.get_post_by_id_and_author(post_id=post_id, author_id=current_user.id)
        return PostResponse.model_validate(db_post)
    except PostNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found or you don't have permission to access it"
        )


@router.put("/posts/{post_id}", response_model=PostResponse)
def update_existing_post(
    post_id: int,
    post_in: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    post_service = PostService(db)
    try:
        updated_post = post_service.update_post(post_id=post_id, author_id=current_user.id, post_in=post_in)
        return PostResponse.model_validate(updated_post)
    except PostNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found or you don't have permission to update it"
        )


@router.delete("/posts/{post_id}", response_model=PostDeleteResponse)
def delete_post_by_id(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    post_service = PostService(db)
    try:
        post_service.delete_post(post_id=post_id, author_id=current_user.id)
        return PostDeleteResponse(message="Post deleted successfully", deleted_post_id=post_id)
    except PostNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found or you don't have permission to delete it"
        )