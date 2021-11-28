from models import User, Post, db 
from app import app

db.drop_all()
db.create_all()