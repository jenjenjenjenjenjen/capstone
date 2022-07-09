import os
from unittest import TestCase

from models import db, connect_db, User, Post, Like, LikePost, Follower, Following

os.environ['DATABASE_URL'] = "postgresql:///capstone-test"

from app import app

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class PublicViewsTestCase(TestCase):
    '''Tests for views for unrestricted pages'''

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
            password='HASHED_PASSWORD'
        )

        db.session.add(self.testuser)
        db.session.commit()

    def test_home_page(self):
        '''Test home page'''

        with self.client as c:

            resp = c.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Popular Movies:', html)

    def test_movie_details(self):
        '''Test movie details page'''

        with self.client as c:

            resp = c.get('/movie/123')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Movie Database', html)

    def test_movie_homepage(self):
        '''Test movie home page'''

        with self.client as c:

            resp = c.get('/movies')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("What's Popular:", html)

    def test_person_page(self):
        '''Test person page'''

        with self.client as c:

            resp = c.get('/person/123')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Movie Database', html)

    def test_tv_details(self):
        '''Test TV details page'''

        with self.client as c:

            resp = c.get('/tv/123')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Movie Database', html)

    def test_tv_homepage(self):
        '''Test TV home page'''

        with self.client as c:

            resp = c.get('/tv')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("What's Popular:", html)

    def test_search(self):
        '''Test search function'''

        with self.client as c:

            resp = c.get('/search?search=marvel')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('marvel', html)