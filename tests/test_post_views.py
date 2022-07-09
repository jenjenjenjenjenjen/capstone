import os
from unittest import TestCase

from models import db, connect_db, User, Post, Like, LikePost, Follower, Following

os.environ['DATABASE_URL'] = "postgresql:///capstone-test"

from app import app

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class PostViewsTestCase(TestCase):
    '''Tests for views for posts'''

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

    def test_new_movie_post(self):
        '''Test add new movie post'''

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.testuser.id

            resp = c.post('/posts/new/movie/123', data={
                'user_id': self.testuser.id,
                'content': 'test',
                'content_id': 123,
                'content_type': 'm'
            })

            post = Post.query.filter_by(user_id=self.testuser.id).first()

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(post.content, 'test')

    def test_new_show_post(self):
        '''Test add new show post'''

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.testuser.id

            resp = c.post('/posts/new/tv/123', data={
                'user_id': self.testuser.id,
                'content': 'test',
                'content_id': 123,
                'content_type': 't'
            })

            post = Post.query.filter_by(user_id=self.testuser.id).first()

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(post.content_type, 't')

    def test_all_user_posts(self):
        '''Test list all user posts'''

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.testuser.id

            resp = c.get('/user/posts')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Movie Database', html)

    def test_user_following_posts(self):
        '''Test user following posts'''

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

            follow = Following(user_id=self.testuser.id, following_id=u.id)

            db.session.add(follow)
            db.session.commit()

            resp = c.get('/user/posts/following')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Following', html)

    def test_delete_post(self):
        '''Test delete post'''
        
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.testuser.id

            post = Post(
                user_id=self.testuser.id,
                content='test',
                content_id=123,
                content_type='m'
            )

            db.session.add(post)
            db.session.commit()

            resp = c.get(f'/posts/{post.id}/delete')

            posts = Post.query.all()

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(posts, [])

    def test_edit_post(self):
        '''Test edit post'''

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.testuser.id

            post = Post(
                user_id=self.testuser.id,
                content='test',
                content_id=123,
                content_type='m'
            )

            db.session.add(post)
            db.session.commit()

            resp = c.post(f'posts/{post.id}/edit', data={
                'content': 'tested'
            })

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(post.content, 'tested')

    def test_like_post(self):
        '''Test like post'''

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.testuser.id

            post = Post(
                user_id=self.testuser.id,
                content='test',
                content_id=123,
                content_type='m'
            )

            db.session.add(post)
            db.session.commit()

            resp = c.post(f'/like/post/{post.id}')

            like = LikePost.query.filter_by(post_id=post.id).first()

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(like.user_id, self.testuser.id)