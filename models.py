"""Models for Blogly."""

from flask import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.kindpng.com/picc/m/24-248253_user-profile-default-image-png-clipart-png-download.png"



class User(db.Model):
    """Site User"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, nullable = False, default = DEFAULT_IMAGE_URL)

    @property
    def full_name(self):
        """Return full name of user"""

        return f"{self.first_name} {self.last_name}"

def connect_db(app):
    """Connect database to Flask app"""

    db.app = app
    db.init_app(app)