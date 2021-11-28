"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def root():
    """Show recent list of posts, most-recent first."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404

#########################
# Routes for Users

@app.route('/users')
def users_list():
    """Show a list of all users"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users = users)

@app.route('/users/new', methods = ["GET"])
def new_user_form():
    """Show a form to create a new user"""

    return render_template('users/new.html')

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

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show form to edit user info"""

    user = User.query.get_or_404(user_id)

    return render_template('users/edit.html', user = user)

@app.route('/users/<int:user_id>/edit', methods = ["POST"])
def update_user(user_id):
    """Form submission for updating a existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods = ["POST"])
def delete_user(user_id):
    """Form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

#########################
# Routes for Posts

@app.route('/users/<int:user_id>/posts/new')
def post_new_form(user_id):
    """Show a form to create a new post for user"""

    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user = user)

@app.route('/users/<int:user_id>/posts/new', methods = ["POST"])
def new_post(user_id):
    """Create a new post upon form submission for user"""

    user = User.query.get_or_404(user_id)
    new_post = Post(title = request.form['title'],
                    content = request.form['content'],
                    user = user)

    db.session.add(new_post)
    db.session.commit()

    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_posts(post_id):
    """Show post information"""

    post = Post.query.get_or_404(post_id)

    print(post.user_id)
    return render_template('posts/show.html', post = post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Edit existing posts from a user"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post = post)

@app.route('/posts/<int:post_id>/edit', methods = ["POST"])
def update_post(post_id):
    """Update post with new post data"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['title']
    
    db.session.add(post)
    db.session.commit()

    flash(f"Post '{post.title}' updated.")

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods = ["POST"])
def delete_post(post_id):
    """Delete user post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    flash(f"Post '{post.title}' deleted.")

    return redirect(f"/users/{post.user_id}")




    



