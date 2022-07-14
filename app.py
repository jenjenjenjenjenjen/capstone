from crypt import methods
from webbrowser import get
from models import db, connect_db, User, Post, Like, Follower, Following, LikePost
from funcs import get_movie_lists
from flask import Flask, render_template, request, redirect, session, flash
from key import api_key
from forms import NewUserForm, SignInForm, NewPostForm, SearchForm, SelectForm, EditPostForm, EditUserForm
import requests
import random


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///capstone"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "abc123"

connect_db(app)

BASE_URL = 'https://api.themoviedb.org/3'
IMG_URL = 'https://www.themoviedb.org/t/p/w440_and_h660_face'

######### PAGES ANYONE CAN ACCESS #############

@app.route('/')
def home_page():
    '''Show home page'''

    resp_movies = requests.get(f'{BASE_URL}/movie/popular', params={'api_key': api_key, 'page': 1})
    movies = resp_movies.json()
    movie_lists = get_movie_lists(movies)

    resp_shows = requests.get(f'{BASE_URL}/tv/popular', params={'api_key': api_key, 'page': 1})
    tv_shows = resp_shows.json()
    show_lists = get_movie_lists(tv_shows)

    if 'user_id' in session:
        curr_user = User.query.get(session['user_id'])
        return render_template('home.html', movies=movie_lists, tv_shows=show_lists, img_url=IMG_URL, curr_user=curr_user)

    return render_template('home.html', movies=movie_lists, tv_shows=show_lists, img_url=IMG_URL)

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    '''Show information for a movie'''

    if 'user_id' in session:
        curr_user = User.query.get(session['user_id'])

        resp = requests.get(f'{BASE_URL}/movie/{movie_id}', params={'api_key': api_key})
        movie = resp.json()

        resp2 = requests.get(f'{BASE_URL}/movie/{movie_id}/credits', params={'api_key': api_key})
        credits = resp2.json()

        return render_template('movie.html', movie=movie, img_url=IMG_URL, credits=credits, curr_user=curr_user)
    
    else:
        resp = requests.get(f'{BASE_URL}/movie/{movie_id}', params={'api_key': api_key})
        movie = resp.json()

        resp2 = requests.get(f'{BASE_URL}/movie/{movie_id}/credits', params={'api_key': api_key})
        credits = resp2.json()

        return render_template('movie.html', movie=movie, img_url=IMG_URL, credits=credits)

@app.route('/movies')
def movie_home_page():
    '''Show home page for movies'''

    pop_resp = requests.get(f'{BASE_URL}/movie/popular', params={'api_key': api_key})
    popular = pop_resp.json()
    popular_lists = get_movie_lists(popular)

    top_resp = requests.get(f'{BASE_URL}/movie/top_rated', params={'api_key': api_key})
    top_rated = top_resp.json()
    top_lists = get_movie_lists(top_rated)

    playing_resp = requests.get(f'{BASE_URL}/movie/now_playing', params={'api_key': api_key})
    now_playing = playing_resp.json()
    playing_lists = get_movie_lists(now_playing)

    up_resp = requests.get(f'{BASE_URL}/movie/upcoming', params={'api_key': api_key})
    upcoming = up_resp.json()
    upcoming_lists = get_movie_lists(upcoming)

    return render_template('movie_home.html', popular=popular_lists, top_rated=top_lists, now_playing=playing_lists, upcoming=upcoming_lists, img_url=IMG_URL)

@app.route('/person/<int:person_id>')
def person_details(person_id):
    '''Show information for a person'''

    resp = requests.get(f'{BASE_URL}/person/{person_id}', params={'api_key': api_key})
    person = resp.json()

    resp2 = requests.get(f'{BASE_URL}/person/{person_id}/movie_credits', params={'api_key': api_key})
    movie_credits = resp2.json()

    resp3 = requests.get(f'{BASE_URL}/person/{person_id}/tv_credits', params={'api_key': api_key})
    tv_credits = resp3.json()

    return render_template('person.html', person=person, movie_credits=movie_credits, tv_credits=tv_credits, img_url=IMG_URL)

@app.route('/tv/<int:show_id>')
def show_details(show_id):
    '''Show details about a TV show'''

    if 'user_id' in session:
        user = User.query.get(session['user_id'])

        resp = requests.get(f'{BASE_URL}/tv/{show_id}', params={'api_key': api_key})
        show = resp.json()

        resp2 = requests.get(f'{BASE_URL}/tv/{show_id}/credits', params={'api_key': api_key})
        credits = resp2.json()

        return render_template('show.html', show=show, credits=credits, curr_user=user, img_url=IMG_URL)
    
    else:
        resp = requests.get(f'{BASE_URL}/tv/{show_id}', params={'api_key': api_key})
        show = resp.json()

        resp2 = requests.get(f'{BASE_URL}/tv/{show_id}/credits', params={'api_key': api_key})
        credits = resp2.json()

        return render_template('show.html', show=show, credits=credits, img_url=IMG_URL)

@app.route('/tv')
def show_tv_home():
    '''Show home page for TV shows'''

    pop_resp = requests.get(f'{BASE_URL}/tv/popular', params={'api_key': api_key})
    popular = pop_resp.json()
    popular_lists = get_movie_lists(popular)

    top_resp = requests.get(f'{BASE_URL}/tv/top_rated', params={'api_key': api_key})
    top_rated = top_resp.json()
    top_lists = get_movie_lists(top_rated)

    today_resp = requests.get(f'{BASE_URL}/tv/airing_today', params={'api_key': api_key})
    airing_today = today_resp.json()
    today_lists = get_movie_lists(airing_today)

    on_air_resp = requests.get(f'{BASE_URL}/tv/on_the_air', params={'api_key': api_key})
    on_air = on_air_resp.json()
    on_air_lists = get_movie_lists(on_air)

    return render_template('tv_home.html', popular=popular_lists, top_rated=top_lists, airing_today=today_lists, on_air=on_air_lists, img_url=IMG_URL)

########## LOG IN/LOGOUT #############

@app.route('/register', methods=["GET", "POST"])
def register_user():
    '''Register a new user'''

    form = NewUserForm()

    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        password = form.password.data

        new_user = User.register(name, username, password)

        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = new_user.id
        flash('Welcome! Successfully created your account!')

        return redirect('/')

    return render_template('register.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def sign_in_user():
    '''Sign in returning user'''

    form = SignInForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f'Welcome back, {user.name}!')
            session['user_id'] = user.id
            return redirect('/')
        else:
            form.username.errors = ["Invalid username/password."]
    
    return render_template('signin.html', form=form)

@app.route('/logout')
def logout_user():
    '''Logout user'''

    if 'user_id' not in session:
        flash('Already logged out!')
        return redirect('/')
        
    session.pop('user_id')
    flash('Successfully logged out!')
    return redirect('/')

@app.route('/user/profile')
def show_user_profile():
    '''Show user profile'''

    if 'user_id' not in session:
        flash('Access unauthorized! Please log in or sign up.')
        return redirect('/')
    
    user_id = session['user_id']

    user = User.query.get(user_id)
    m_likes = Like.query.filter_by(content_type='m').all()
    s_likes = Like.query.filter_by(content_type='t').all()

    movies = []
    shows = []

    for like in m_likes:
        resp = requests.get(f'{BASE_URL}/movie/{like.movie_id}', params={'api_key': api_key})
        movie = resp.json()
        movies.append(movie)

    for like in s_likes:
        resp = requests.get(f'{BASE_URL}/tv/{like.movie_id}', params={'api_key': api_key})
        show = resp.json()
        shows.append(show)

    return render_template('profile.html', user=user, img_url=IMG_URL, shows=shows, movies=movies)

@app.route('/user/profile/edit', methods=['GET', 'POST'])
def edit_user():
    '''Edit user info'''

    if 'user_id' not in session:
        flash('Access unauthorized! Please log in or sign up.')
        return redirect('/')

    form = EditUserForm()
    user = User.query.get(session['user_id'])

    if form.validate_on_submit():
        if User.authenticate(
            username=user.username,
            password=form.password.data
        ):
            user.name = form.name.data
            user.username = form.username.data
            db.session.commit()
            flash('Changes saved!', 'success')
            return redirect('/user/profile')
        else:
            flash('Invalid password!', 'error')
            return redirect('/user/profile')

    return render_template('edit_user.html', form=form, user=user)

############# USER INFO ###############

@app.route('/user/<int:user_id>')
def show_user_details(user_id):
    '''Show profile for other users'''

    if 'user_id' not in session:
        flash('Access unauthorized! Please log in or sign up.')
        return redirect('/')

    user = User.query.get_or_404(user_id)
    curr_user = User.query.get(session['user_id'])

    return render_template('user_profile.html', user=user, curr_user=curr_user)

@app.route('/follow/<int:user_id>', methods=['POST'])
def follow_user(user_id):
    '''Follow another user'''

    if 'user_id' not in session:
        flash('Access unauthorized! Please log in or sign up.')
        return redirect('/')

    curr_user = User.query.get(session['user_id'])
    user_to_follow = User.query.get_or_404(user_id)

    new_follow = Follower(user_id=user_to_follow.id, follower_id=curr_user.id)
    db.session.add(new_follow)
    db.session.commit()

    new_following = Following(user_id=curr_user.id, following_id=user_to_follow.id)
    db.session.add(new_following)
    db.session.commit()

    flash(f'You are now following @{user_to_follow.username}')
    return redirect('/')

@app.route('/unfollow/<int:user_id>', methods=['POST'])
def unfollow_user(user_id):
    '''Unfollow a user'''

    if 'user_id' not in session:
        flash('Access unauthorized! Please log in or sign up.')
        return redirect('/')

    curr_user = User.query.get(session['user_id'])
    user_to_unfollow = User.query.get_or_404(user_id)

    for following in curr_user.following:
        if user_to_unfollow.id == following.following_id:
            follow = Following.query.get(following.id)
            db.session.delete(follow)
            db.session.commit()

    for followers in user_to_unfollow.followers:
        if curr_user.id == followers.follower_id:
            follow = Follower.query.get(followers.id)
            db.session.delete(follow)
            db.session.commit()

    flash(f'You have unfollowed @{user_to_unfollow.username}')
    return redirect('/')

######## LIKE MOVIES AND SHOWS #############

@app.route('/like/<int:movie_id>', methods=['POST'])
def like_movie(movie_id):
    '''Like a movie'''

    if 'user_id' not in session:
        flash('Access unauthorized! Please log in or sign up.')
        return redirect(f'/movie/{movie_id}')

    user = User.query.get(session['user_id'])

    for like in user.likes:
        if like.movie_id == movie_id:
            unlike = Like.query.get(like.id)

            db.session.delete(unlike)
            db.session.commit()

            return redirect(f'/movie/{movie_id}')

    new_like = Like(movie_id=movie_id, user_id=user.id, content_type='m')
    db.session.add(new_like)
    db.session.commit()

    flash('Liked!')
    return redirect(f'/movie/{movie_id}')

@app.route('/like/show/<int:show_id>', methods=['POST'])
def like_show(show_id):
    '''Like a show'''

    if 'user_id' not in session:
        flash('Access unauthorized! Please log in or sign up.')
        return redirect(f'/tv/{show_id}')

    user = User.query.get(session['user_id'])

    for like in user.likes:
        if like.movie_id == show_id:
            unlike = Like.query.get(like.id)

            db.session.delete(unlike)
            db.session.commit()

            return redirect(f'/tv/{show_id}')

    new_like = Like(movie_id=show_id, user_id=user.id, content_type='t')
    db.session.add(new_like)
    db.session.commit()

    flash('Liked!')
    return redirect(f'/tv/{show_id}')

######## POSTS #############

@app.route('/posts/new', methods=['GET', 'POST'])
def show_new_post_form():
    '''Display new post form'''

    if 'user_id' not in session:
        flash('Access unauthorized! Please log in or sign up.')
        return redirect('/)')

    form = NewPostForm()
    search_form = SearchForm()
    select_form = SelectForm()

    if search_form.validate_on_submit():

        movie_or_tv = search_form.content_type.data
        search = search_form.search.data

        if movie_or_tv == 'movie':
            resp = requests.get(f'{BASE_URL}/search/movie', params={'api_key': api_key, 'query': search})
            movie = resp.json()
    
            return render_template('new_post.html', movie_or_tv=movie_or_tv, img_url=IMG_URL, search=search, form=form, search_form=search_form, movie=movie, select_form=select_form)
        if movie_or_tv == 'show':
            resp = requests.get(f'{BASE_URL}/search/tv', params={'api_key': api_key, 'query': search})
            movie = resp.json()

            return render_template('new_post.html', movie_or_tv=movie_or_tv, img_url=IMG_URL, search=search, form=form, search_form=search_form, movie=movie, select_form=select_form)
   
    if select_form.validate_on_submit():
        
        movie_id = select_form.movie_id.data
        content_type = select_form.movie_or_tv.data
    
        if content_type == 'movie':
            
            resp = requests.get(f'{BASE_URL}/movie/{movie_id}', params={'api_key': api_key})
            movie = resp.json()

            return render_template('new_post.html', content_type=content_type, selected_movie=movie, img_url=IMG_URL, form=form, search_form=search_form, movie=movie, select_form=select_form)

        if content_type == 'show':

            resp = requests.get(f'{BASE_URL}/tv/{movie_id}', params={'api_key': api_key})
            movie = resp.json()

            return render_template('new_post.html', content_type=content_type, selected_movie=movie, img_url=IMG_URL, form=form, search_form=search_form, movie=movie, select_form=select_form)

    if form.validate_on_submit():
        
        try:
            content = form.content.data
            content_id = form.movie_id.data
            type = form.type.data

            new_post = Post(user_id=session['user_id'], content=content, content_id=content_id, content_type=type)

            db.session.add(new_post)
            db.session.commit()

            return redirect('/user/posts')
        
        except:
            flash('Please select a movie or TV show!')
            return redirect('/posts/new')

    return render_template('new_post.html', form=form, search_form=search_form, select_form=select_form)

@app.route('/posts/new/movie/<int:id>', methods=['GET', 'POST'])
def new_movie_post(id):
    '''Make a new post from pre-selected movie'''

    if 'user_id' not in session:
        flash('Access unauthorized! Please log in or sign up.')
        return redirect('/')

    resp = requests.get(f'{BASE_URL}/movie/{id}', params={'api_key': api_key})
    movie = resp.json()

    form = NewPostForm()

    if form.validate_on_submit():

        content = form.content.data
        content_id = id
        type = 'm'

        new_post = Post(user_id=session['user_id'], content=content, content_id=content_id, content_type=type)

        db.session.add(new_post)
        db.session.commit()

        return redirect('/user/posts')

    return render_template('movie_post.html', movie=movie, form=form, img_url=IMG_URL)

@app.route('/posts/new/tv/<int:id>', methods=['GET', 'POST'])
def new_tv_post(id):
    '''Make a new post from pre-selected show'''

    if 'user_id' not in session:
        flash('Access unauthorized! Please log in or sign up.')
        return redirect('/')

    resp = requests.get(f'{BASE_URL}/tv/{id}', params={'api_key': api_key})
    movie = resp.json()

    form = NewPostForm()

    if form.validate_on_submit():

        content = form.content.data
        content_id = id
        type = 't'

        new_post = Post(user_id=session['user_id'], content=content, content_id=content_id, content_type=type)

        db.session.add(new_post)
        db.session.commit()

        return redirect('/user/posts')

    return render_template('movie_post.html', movie=movie, form=form, img_url=IMG_URL)

@app.route('/user/posts')
def show_posts():
    '''Show users posts'''

    posts = Post.query.all()

    curr_user = User.query.get(session['user_id'])

    all_post_details = []

    for post in posts:
        if post.content_type == 'm':
            resp = requests.get(f'{BASE_URL}/movie/{post.content_id}', params={'api_key': api_key})
            post_details = resp.json()
            all_post_details.append(post_details)

        if post.content_type == 't':
            resp = requests.get(f'{BASE_URL}/tv/{post.content_id}', params={'api_key': api_key})
            post_details = resp.json()
            all_post_details.append(post_details)
    return render_template('posts.html', posts=posts, post_details=all_post_details, img_url=IMG_URL, curr_user=curr_user)

@app.route('/user/posts/following')
def show_following_posts():
    '''Show user posts from users they're following'''

    posts = Post.query.all()

    curr_user = User.query.get(session['user_id'])

    all_post_details = []

    if curr_user.following:
        for user in curr_user.following:
            following_id = user.following_id
            user_select = User.query.get(following_id)
            for post in user_select.posts:
                if post.content_type == 'm':
                    resp = requests.get(f'{BASE_URL}/movie/{post.content_id}', params={'api_key': api_key})
                    post_details = resp.json()
                    all_post_details.append(post_details)

                if post.content_type == 't':
                    resp = requests.get(f'{BASE_URL}/tv/{post.content_id}', params={'api_key': api_key})
                    post_details = resp.json()
                    all_post_details.append(post_details)

            return render_template('posts.html', post_details=all_post_details, posts=posts, img_url=IMG_URL, curr_user=curr_user)
    else:
        flash('Not following anyone!')
        return redirect('/user/posts')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    '''Delete a post'''

    if 'user_id' not in session:
        flash('Access unauthorized! Please log in or sign up.')
        return redirect('/')

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    flash('Post deleted!')
    return redirect('/user/posts')

@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    '''Edit a post'''

    if 'user_id' not in session:
        flash('Access unauthorized! Please log in or sign up.')
        return redirect('/')

    post = Post.query.get_or_404(post_id)
    if post.content_type == 'm':
        resp = requests.get(f'{BASE_URL}/movie/{post.content_id}', params={'api_key': api_key})
        post_details = resp.json()

    if post.content_type == 't':
        resp = requests.get(f'{BASE_URL}/tv/{post.content_id}', params={'api_key': api_key})
        post_details = resp.json()

    form = EditPostForm()

    if form.validate_on_submit():
        content = form.content.data

        post.content = content
        db.session.commit()
        return redirect('/user/posts')

    return render_template('edit_post.html', post=post, form=form, img_url=IMG_URL, post_details=post_details)

@app.route('/user/<int:user_id>/posts')
def show_user_posts(user_id):
    '''Show posts for a certain user'''

    user = User.query.get_or_404(user_id)
    curr_user = User.query.get(session['user_id'])
    posts = Post.query.all()
    content = []

    for post in posts:
        if post.user_id == user_id:
            if post.content_type == 'm':
                resp = requests.get(f'{BASE_URL}/movie/{post.content_id}', params={'api_key': api_key})
                post_details = resp.json()
                content.append(post_details)

            if post.content_type == 't':
                resp = requests.get(f'{BASE_URL}/tv/{post.content_id}', params={'api_key': api_key})
                post_details = resp.json()
                content.append(post_details)
    
    return render_template('profile_posts.html', user=user, curr_user=curr_user, content=content, img_url=IMG_URL)

@app.route('/user/<int:user_id>/likes')
def show_user_likes(user_id):
    '''Show posts a certain user has liked'''

    user = User.query.get_or_404(user_id)
    curr_user = User.query.get(session['user_id'])
    content = []

    for like in user.likes_posts:
        if like.post.content_type == 'm':
            resp = requests.get(f'{BASE_URL}/movie/{like.post.content_id}', params={'api_key': api_key})
            details = resp.json()
            content.append(details)
        if like.post.content_type == 't':
            resp = requests.get(f'{BASE_URL}/tv/{like.post.content_id}', params={'api_key': api_key})
            details = resp.json()
            content.append(details)
    
    return render_template('profile_likes.html', user=user, curr_user=curr_user, content=content, img_url=IMG_URL)

@app.route('/user/<int:user_id>/following')
def show_user_following(user_id):
    '''Show users that another user is following'''

    user = User.query.get_or_404(user_id)
    curr_user = User.query.get(session['user_id'])
    following = user.following

    return render_template('user_following.html', user=user, following=following, curr_user=curr_user)

@app.route('/user/<int:user_id>/followers')
def show_user_followers(user_id):
    '''Show a users followers'''

    user = User.query.get_or_404(user_id)
    curr_user = User.query.get(session['user_id'])
    followers = user.followers

    return render_template('user_followers.html', user=user, followers=followers, curr_user=curr_user)

@app.route('/like/post/<int:post_id>', methods=['POST'])
def like_post(post_id):
    '''Like a post'''

    if 'user_id' not in session:
        flash('Access unauthorized! Please log in or sign up.')
        return redirect('/')

    user = User.query.get(session['user_id'])

    for like in user.likes_posts:
        if like.post_id == post_id:
            unlike = LikePost.query.get(like.id)

            db.session.delete(unlike)
            db.session.commit()
            flash('Unliked!')
            return redirect('/user/posts')

    new_like = LikePost(user_id=user.id, post_id=post_id)

    db.session.add(new_like)
    db.session.commit()
    flash('Liked!')
    return redirect('/user/posts')

@app.route('/search')
def search_content():
    '''Search for a movie or show'''

    search = request.args['search']

    resp = requests.get(f'{BASE_URL}/search/multi', params={'api_key': api_key, 'query': search})
    results = resp.json()

    return render_template('search.html', search=search, results=results, img_url=IMG_URL)