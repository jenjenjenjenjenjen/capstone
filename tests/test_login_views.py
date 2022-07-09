import os
from unittest import TestCase

from models import db, connect_db, User, Post, Like, LikePost, Follower, Following

os.environ['DATABASE_URL'] = "postgresql:///capstone-test"

from app import app

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class LoginViewsTestCase(TestCase):
    '''Tests for views for log in pages'''

    def setUp(self):
        '''Create test client, add sample data'''

        Following.query.delete()
        Follower.query.delete()
        LikePost.query.delete()
        Like.query.delete()
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

    def test_register_user(self):
        '''Test registration page'''

        with self.client as c:

            resp = c.get('/register')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Sign up to share', html)

            resp = c.post('/register', data={
                "name": 'test',
                "username": 'testuser',
                "password": 'testuser'
            })

            self.assertEqual(resp.status_code, 302)

    def test_sign_in(self):
        '''Test user sign in'''

        with self.client as c:

            resp = c.get('/signin')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Sign Up', html)

            u = User.register(
                name='test',
                username='testuser',
                password='password'
            )

            db.session.add(u)
            db.session.commit()

            resp = c.post('/signin', data={
                "username": 'testuser',
                "password": 'password'
            })

            self.assertEqual(resp.status_code, 302)

    def test_logout(self):
        '''Test logout'''

        with self.client as c:

            u = User.register(
                name='test',
                username='testuser',
                password='password'
            )

            db.session.add(u)
            db.session.commit()

            with c.session_transaction() as sess:
                sess['user_id'] = u.id

            resp = c.get('/logout')

            self.assertEqual(resp.status_code, 302)