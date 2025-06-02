from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import time

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate
from app.crud import post as post_crud 
from app.core.config import settings
from app.utils.exceptions import PostNotFoundError

posts_cache: Dict[int, Dict[str, Any]] = {}


class PostService:

    def __init__(self, db: Session):
        self.db = db

    def create_post(self, post_in: PostCreate, author_id: int) -> Post:

        db_post = post_crud.create_post_db(self.db, post_in.text, author_id)
        
        if author_id in posts_cache:
            del posts_cache[author_id]
            
        return db_post

    def get_posts_by_author(self, author_id: int) -> List[Post]:

        current_time = time.time()
        cache_expiry = settings.cache_expire_minutes * 60

        if author_id in posts_cache and (current_time - posts_cache[author_id]["timestamp"]) < cache_expiry:
            print(f"Returning posts for user {author_id} from cache.")
            return posts_cache[author_id]["posts"]

        db_posts = post_crud.get_posts_by_author_db(self.db, author_id)
        
        posts_cache[author_id] = {
            "posts": db_posts,
            "timestamp": current_time
        }
        print(f"Fetching posts for user {author_id} from DB and caching.")
        return db_posts

    def get_post_by_id_and_author(self, post_id: int, author_id: int) -> Post:
  
        db_post = post_crud.get_post_by_id_and_author_db(self.db, post_id, author_id)
        if not db_post:
            raise PostNotFoundError(f"Post with ID {post_id} not found for author {author_id}.")
        return db_post

    def update_post(self, post_id: int, author_id: int, post_in: PostUpdate) -> Post:

        db_post = self.get_post_by_id_and_author(post_id, author_id) 
        
        updated_post = post_crud.update_post_db(self.db, db_post, post_in.text)
        
        if db_post.author_id in posts_cache:
            del posts_cache[db_post.author_id]
            
        return updated_post

    def delete_post(self, post_id: int, author_id: int):

        db_post = self.get_post_by_id_and_author(post_id, author_id) 
        
        author_id_to_invalidate = db_post.author_id 
        post_crud.delete_post_db(self.db, db_post)
        
        if author_id_to_invalidate in posts_cache:
            del posts_cache[author_id_to_invalidate]
            
        return True