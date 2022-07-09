from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    '''Create User model'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)

    @classmethod
    def register(cls, name, username, password):
        '''Register a new user'''

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        return cls(name=name, username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, password):
        '''Authenticate a returning user'''

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False

class Post(db.Model):
    '''Create Post model'''

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text)
    content_id = db.Column(db.Integer)
    content_type = db.Column(db.Text)
    
    user = db.relationship('User', backref='posts')

class Like(db.Model):
    '''Create Like model'''

    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_type = db.Column(db.Text)

    user = db.relationship('User', backref='likes')

class LikePost(db.Model):
    '''Create Like Post model'''

    __tablename__ = 'likes_posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    user = db.relationship('User', backref='likes_posts')
    post = db.relationship('Post', backref='likes_posts')

class Follower(db.Model):
    '''Create Follower model'''

    __tablename__ = 'followers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', foreign_keys=[user_id], backref='followers')
    follower = db.relationship('User', foreign_keys=[follower_id])

class Following(db.Model):
    '''Create Following model'''

    __tablename__ = 'following'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    following_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', foreign_keys=[user_id], backref='following')
    following = db.relationship('User', foreign_keys=[following_id])