import os
from unittest import TestCase

from models import db, User, Post, LikePost, Like, Follower, Following

os.environ['DATABASE_URL'] = "postgresql:///capstone-test"

from app import app

db.create_all

class FollowingModelTestCase(TestCase):
    '''Test following model'''

    def setUp(self):
        '''Create test client'''

        LikePost.query.delete()
        Post.query.delete()
        Follower.query.delete()
        Following.query.delete()
        Like.query.delete()
        User.query.delete()

        self.client = app.test_client()

        u = User(
            name='test',
            username='testuser',
            password='HASHED_PASSWORD'
        )

        db.session.add(u)
        db.session.commit()

        u2 = User(
            name='test2',
            username='testuser2',
            password='HASHED_PASSWORD'
        )

        db.session.add(u2)
        db.session.commit()

    def test_following_model(self):
        '''Test basic following model'''

        u1 = User.query.filter_by(username='testuser').first()
        u2 = User.query.filter_by(username='testuser2').first()

        f = Following(user_id=u2.id, following_id=u1.id)

        db.session.add(f)
        db.session.commit()

        self.assertEqual(len(u1.following), 0)
        self.assertEqual(len(u2.following), 1)
        self.assertIsInstance(f, Following)