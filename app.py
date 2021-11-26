"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

@app.route('/')
def route():
    """Redirects to a list of users"""

    return redirect('/users')

@app.route('/users')
def users_list():
    """Show a list of all users"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users = users)

@app.route('/users/new', methods = ["GET"])
def new_user_form():
    """Show a form to create a new user"""

    return render_template('user/new.html')

@app.route('/users/new', methods = ["POST"])
def users_new():
    """Form submission for a new user"""

    new_user = User(first_name = request.form['first_name'],
                    last_name = request.form['last_name'],
                    image_url = request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_users(user_id):
    """Show a page with info of user"""

    user = User.query.get_or_404(user_id)

    return render_template('/users/show.html', user = user)

@app.route('users/<id:user_id>/edit')
def edit_user(user_id):
    """Show form to edit user info"""

    user = User.query.get_or_404(user_id)

    return render_template('users/edit.html', user = user)

@app.route('users/<int:user_id/edit>', methods = ["POST"])
def update_user(user_id):
    """Form submission for updating a existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('users/<int:user_id/delete>', methods = ["POST"])
def delete_user(user_id):
    """Form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')