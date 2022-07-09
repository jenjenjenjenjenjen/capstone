import os
from unittest import TestCase

from models import db, connect_db, User, Post, Like, LikePost, Follower, Following

os.environ['DATABASE_URL'] = "postgresql:///capstone-test"

from app import app

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserViewsTestCase(TestCase):
    '''Tests for views for user pages'''

    def setUp(self):
        '''Create test client, add sample data'''

        Following.query.delete()
        Follower.query.delete()
        LikePost.query.delete()
        Like.query.delete()
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        self.testuser = User.register(
            name='test',
            username='testuser',
            password='password'
        )

        db.session.add(self.testuser)
        db.session.commit()

    def test_user_profile(self):
        '''Test user profile view'''

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.testuser.id

            resp = c.get('/user/profile')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit Profile', html)

    def test_other_profiles(self):
        '''Test user view other profiles'''

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.testuser.id

            u = User.register(
            name='test2',
            username='testuser2',
            password='password'
            )

            db.session.add(u)
            db.session.commit()

            resp = c.get(f'/user/{u.id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Follow', html)

    def test_follow_user(self):
        '''Test follow function'''

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.testuser.id

            u = User.register(
                name='test2',
                username='testuser2',
                password='password'
            )

            db.session.add(u)
            db.session.commit()

            resp = c.post(f'/follow/{u.id}')

            self.assertEqual(resp.status_code, 302)

            follow = Follower.query.one()
            self.assertEqual(follow.follower_id, self.testuser.id)

            following = Following.query.one()
            self.assertEqual(following.user_id, self.testuser.id)

    def test_unfollow_user(self):
        '''Test unfollow user'''

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.testuser.id

            u = User.register(
                name='test2',
                username='testuser2',
                password='password'
            )

            db.session.add(u)
            db.session.commit()

            c.post(f'/follow/{u.id}')

            resp = c.post(f'/unfollow/{u.id}')

            self.assertEqual(resp.status_code, 302)

    def test_like_movie(self):
        '''Test like movie'''

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.testuser.id

            resp = c.post('/like/123')

            like = Like.query.filter_by(user_id=self.testuser.id).first()

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(like.movie_id, 123)

    def test_like_show(self):
        '''Test like show'''

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.testuser.id

            resp = c.post('/like/show/123')

            like = Like.query.filter_by(content_type='t').first()

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(like.movie_id, 123)

    def test_profile_posts(self):
        '''Test posts on a users profile'''

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.testuser.id

            resp = c.get(f'/user/{self.testuser.id}/posts')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.testuser.name, html)

    def test_profile_likes(self):
        '''Test user likes in profile'''

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.testuser.id

            resp = c.get(f'/user/{self.testuser.id}/likes')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Likes', html)

    def test_user_following(self):
        '''Test user list user following'''

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.testuser.id

            resp = c.get(f'/user/{self.testuser.id}/following')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Following', html)

    def test_user_followers(self):
        '''Test list user followers'''

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.testuser.id

            resp = c.get(f'/user/{self.testuser.id}/followers')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Followers', html)