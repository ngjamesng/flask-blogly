from app import app
from unittest import TestCase
from models import default_img_url, db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test_3"
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class RoutesTestCase(TestCase):
    """ Integration tests for our routes """

    def setUp(self):
        db.drop_all()
        db.create_all()

        # Add dummy users
        whiskey = User(first_name='Whiskey', last_name='Lane',
                       img_url='https://www.rithmschool.com/assets/team/whiskey-4afaa4064090599efd8501e7693464d3968d036a0b683407611c746a9e4d732a.jpg')
        nicholai = User(first_name='Nicholai', last_name='Hansen')
        james = User(first_name='James', last_name='Ng')

        # Add new users to session
        db.session.add(whiskey)
        db.session.add(nicholai)
        db.session.add(james)

        # Commmit
        db.session.commit()

        # Add dummy posts
        whiskey_post = Post(title='I\'m a dog',
                            content='woof', user_id=whiskey.id)
        james_post = Post(
            title='Testing', content='Paragraph', user_id=james.id)

        # Add new posts
        db.session.add(whiskey_post)
        db.session.add(james_post)

        # Commmit
        db.session.commit()

    def test_show_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Whiskey', html)
            self.assertIn('Nicholai', html)

    def test_show_new_user_form(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Create a user', html)

    def test_create_new_user(self):
        with app.test_client() as client:
            resp = client.post('/users/new',
                               data={'first-name': 'Jimmy',
                                     'last-name': 'Peach',
                                     'img-url': default_img_url},
                               follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Jimmy', html)
            self.assertIn("https://images.unsplash.com/photo-1580329", html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get('/users/1')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Whiskey', html)

    def test_show_edit_user_form(self):
        with app.test_client() as client:
            resp = client.get('/users/2/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Nicholai', html)
            self.assertIn('Edit a user', html)

    def test_update_user(self):
        with app.test_client() as client:
            resp = client.post('/users/3/edit',
                               data={'first-name': 'King',
                                     'last-name': 'James',
                                     'img-url': default_img_url},
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('King', html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post('/users/3/delete',
                               follow_redirects=True)
            print("RESPONSE >>>>", resp)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('James', html)

    def test_show_create_post_form(self):
        with app.test_client() as client:
            resp = client.get('/users/1/posts/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add Post for Whiskey', html)

    def test_create_new_post(self):
        with app.test_client() as client:
            resp = client.post('/users/1/posts/new',
                               data={'title': 'I\'m a god',
                                     'content': 'Dyslexia is fun'},
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('a god', html)
            self.assertIn('Whiskey', html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get('/posts/1')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('woof', html)
            self.assertIn('Whiskey', html)

    def test_show_edit_post_form(self):
        with app.test_client() as client:
            resp = client.get('/posts/2/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Testing', html)

    def test_update_post(self):
        with app.test_client() as client:
            resp = client.post('/posts/2/edit',
                               data={'title': 'Changed',
                                     'content': 'Different content'},
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Different content', html)
            self.assertIn('James', html)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post('/posts/1/delete',
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('a dog', html)
