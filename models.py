"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.kindpng.com/picc/m/24-248253_user-profile-default-image-png-clipart-png-download.png"



class User(db.Model):
    """Site User"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, nullable = False, default = DEFAULT_IMAGE_URL)

    posts = db.relationship("Post", backref = "user", cascade = "all, delete-orphan")

    def __repr__(self):

        return f"<{self.first_name} {self.last_name}>"

    @property
    def full_name(self):
        """Return full name of user"""

        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Model for User Posts"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    def __repr__(self):
        return f"{self.title}; Content: {self.content}"

    @property
    def format_date(self):
        """Return better-formated date"""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")



def connect_db(app):
    """Connect database to Flask app"""

    db.app = app
    db.init_app(app)