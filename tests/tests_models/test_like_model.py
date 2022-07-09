import os
from unittest import TestCase

from models import db, User, Post, LikePost, Like, Follower, Following

os.environ['DATABASE_URL'] = "postgresql:///capstone-test"

from app import app

db.create_all

class LikeModelTestCase(TestCase):
    '''Test like model'''

    def setUp(self):
        '''Create test client'''

        Post.query.delete()
        LikePost.query.delete()
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

    def test_like_model(self):
        '''Test basic like model'''

        u = User.query.filter_by(username='testuser').first()

        l = Like(
            movie_id=123,
            user_id=u.id,
            content_type='m'
        )

        db.session.add(l)
        db.session.commit()

        self.assertEqual(len(u.likes), 1)
        self.assertIsInstance(l, Like)