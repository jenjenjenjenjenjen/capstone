import os
from unittest import TestCase

from models import db, User, Post, LikePost, Like, Follower, Following

os.environ['DATABASE_URL'] = "postgresql:///capstone-test"

from app import app

db.create_all

class UserModelTestCase(TestCase):
    '''Test user model'''

    def setUp(self):
        '''Create test client'''

        Post.query.delete()
        LikePost.query.delete()
        Follower.query.delete()
        Following.query.delete()
        Like.query.delete()
        User.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        '''Does basic model work?'''

        u = User(
            name='test',
            username='testuser',
            password='HASHED_PASSWORD'
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.likes_posts), 0)
        self.assertEqual(len(u.followers), 0)

    def test_user_create(self):
        '''Test success of whether a user is created'''

        u1 = User(
            name='test',
            username='testuser',
            password='HASHED_PASSWORD'
        )
        u2 = User(
            name='test2',
            password='HASHED_PASSWORD'
        )

        self.assertIsInstance(u1, User)
        self.assertIsNone(u2.username)

    def test_authenticate_method(self):
        '''Test if user is authenticated '''

        u = User.register(
            name='test',
            username='testuser',
            password='HASHED_PASSWORD'
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(u.authenticate(username='testuser', password='HASHED_PASSWORD'), u)
        self.assertFalse(u.authenticate(username='bob', password='HASHED_PASSWORD'), u)
        self.assertFalse(u.authenticate(username='testuser', password='wrong_password'))