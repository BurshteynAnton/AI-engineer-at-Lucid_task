import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.database import Base, engine 
from app.models import user, post 

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")