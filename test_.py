from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class BloglyTestCase(TestCase):
    """Tests for Blogly view functions"""

    def setUp(self):
        """Add sample user and post"""

        user = User(first_name = "Test",
                    last_name = "User",
                    image_url = "https://www.kindpng.com/picc/m/24-248253_user-profile-default-image-png-clipart-png-download.png")


        self.user_id = user.id
        self.user = user

        post = Post(title = 'Post1',
                    content = 'Post 1 content',
                    user_id = 1)
                    

        self.post_id = post.id
        self.post = post

        db.session.add(user)
        db.session.add(post)
        db.session.commit()

    def tearDown(self):
        """Clean up any bad transactions"""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)

    def test_show_new_user_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Create New User", html)
            self.assertIn("First Name", html)

    def test_add_new_user(self):
        with app.test_client() as client:
            d = {"first_name": "Test1", "last_name": "User1", "image_url": "https://static.onecms.io/wp-content/uploads/sites/28/2021/02/11/chicago-illinois-CHITG0221.jpg"}
            resp = client.post("/users/new", data = d, follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test1 User1", html)

    def test_delete_user(self):
        with app.test_client() as client:
            d = {"first_name": "Test", "last_name": "User1", "image_url": "https://www.kindpng.com/picc/m/24-248253_user-profile-default-image-png-clipart-png-download.png"}
            resp = client.post("/users/2/delete", data = d, follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Test1 User1", html)

    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": "Upper Side Dreamin", "content": "upperside dreamin yeah", "user_id": 2}
            resp = client.post("/users/2/posts/new", data = d, follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            
