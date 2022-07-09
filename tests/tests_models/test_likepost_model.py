import os
from unittest import TestCase

from models import db, User, Post, LikePost, Like, Follower, Following

os.environ['DATABASE_URL'] = "postgresql:///capstone-test"

from app import app

db.create_all

class LikePostModelTestCase(TestCase):
    '''Test likepost model'''

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

        p = Post(
            user_id=u.id,
            content='test',
            content_id=123,
            content_type='m'
        )

        db.session.add(p)
        db.session.commit()

    def test_likepost_model(self):
        '''Test basic likepost model'''

        u = User.query.filter_by(username='testuser').first()
        p = Post.query.filter_by(content='test').first()

        l = LikePost(
            user_id=u.id,
            post_id=p.id
        )

        db.session.add(l)
        db.session.commit()

        self.assertEqual(len(u.likes_posts), 1)
        self.assertEqual(len(p.likes_posts), 1)
        self.assertIsInstance(l, LikePost)