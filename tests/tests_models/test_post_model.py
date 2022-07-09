import os
from unittest import TestCase

from models import db, User, Post, LikePost, Like, Follower, Following

os.environ['DATABASE_URL'] = "postgresql:///capstone-test"

from app import app

db.create_all

class PostModelTestCase(TestCase):
    '''Test post model'''

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

    def test_post_model(self):
        '''Test basic post model'''

        u = User.query.filter_by(username='testuser').first()

        p = Post(
            user_id=u.id,
            content='test',
            content_id='123',
            content_type='m'
        )

        db.session.add(p)
        db.session.commit()

        self.assertEqual(len(u.posts), 1)
        self.assertIsInstance(p, Post)