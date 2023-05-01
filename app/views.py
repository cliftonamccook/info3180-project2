"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""
import os
import jwt
from datetime import datetime, timedelta
from functools import wraps
from time import time
from app import app, db, login_manager
from flask import render_template, request, jsonify, send_file, session, send_from_directory, url_for, redirect, g
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from app.forms import LoginForm, RegistrationForm, NewPostForm
from app.models import User, Post, Follow, Like
from flask_wtf.csrf import generate_csrf


###
# Routing for your application.
###

# Create a JWT @requires_auth decorator
# This decorator can be used to denote that a specific route should check
# for a valid JWT token before displaying the contents of that route.
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None) # or request.cookies.get('token', None)

    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

    except jwt.ExpiredSignatureError:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    g.current_user = user = payload
    return f(*args, **kwargs)

  return decorated


@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/api/v1/register', methods=['POST'])
def register():
    """Accepts user information and saves it to the database"""
    regForm = RegistrationForm()
    if regForm.validate_on_submit():
        username = regForm.username.data
        password = regForm.password.data
        firstname = regForm.firstname.data
        lastname = regForm.lastname.data
        email = regForm.email.data
        location = regForm.location.data
        biography = regForm.biography.data
        photo = regForm.photo.data
        profile_photo = secure_filename(photo.filename)
        joined_on = datetime.utcnow()
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_photo))
        user = User(username,password,firstname,lastname,email,location,biography,profile_photo,joined_on)
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "message": "User successfully registered.",
            "username": username,
            "password": password,
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "location": location,
            "biography": biography,
            "profile_photo": profile_photo,
            "joined_on": joined_on
        }), 201
    errors = form_errors(regForm)
    return jsonify(errors=errors), 400


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """Accepts login credentials as username and password"""
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        uname = loginForm.username.data
        password = loginForm.password.data
        user = db.session.execute(db.select(User).filter_by(username=uname)).scalar()
        if user is not None and check_password_hash(user.password, password):
            login_user(user)
            jwt_token = generate_token(user.id)
            return jsonify({
                "message": "User successfully logged in.",
                "token": jwt_token
            }), 200
        return jsonify(errors=["Invalid username or password"])
    errors = form_errors(loginForm)
    return jsonify(errors=errors), 400


@app.route('/api/v1/auth/logout', methods=['POST'])
@login_required
def logout():
    """Logout a user"""
    logout_user()
    return jsonify({
        "message": "User successfully logged out."
    }), 200


@app.route('/api/v1/users/<user_id>/posts', methods=['POST'])
@login_required
@requires_auth
def add_post(user_id):
    """Used for adding posts to the users feed"""
    postForm = NewPostForm()
    if postForm.validate_on_submit():
        photo = postForm.photo.data
        caption = postForm.caption.data
        photo_filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
        created_on = datetime.utcnow()
        post = Post(caption,photo_filename,user_id,created_on)
        db.session.add(post)
        db.session.commit()
        return jsonify({
            "message": "Successfully created a new post"
        }), 201
    errors = form_errors(postForm)
    return jsonify(errors=errors), 400




@app.route('/api/v1/users/<user_id>', methods=['GET'])
@login_required
@requires_auth
def get_user_details(user_id):
    """Returns user details"""
    user_details = db.session.execute(db.select(User).filter_by(id=int(user_id))).scalar()
    user_posts = db.session.execute(db.select(Post).filter_by(user_id=int(user_id))).scalars()
    posts = []
    for post in user_posts:
        posts.append({
            "id": post.id,
            "user_id": post.user_id,
            "photo": url_for('getImage', filename=post.photo),
            "description": post.caption,
            "created_on": post.created_on,
        })
    return jsonify({
        "id": user_details.id,
        "username": user_details.username,
        "firstname": user_details.firstname,
        "lastname": user_details.lastname,
        "email": user_details.email,
        "location": user_details.location,
        "biography": user_details.biography,
        "profile_photo": url_for('getImage', filename=user_details.profile_photo),
        "joined_on": user_details.joined_on,
        "posts": posts
    }), 200


@app.route('/api/v1/users/<user_id>/posts', methods=['GET'])
@login_required
@requires_auth
def get_posts(user_id):
    """Returns a user's posts"""
    user_posts = db.session.execute(db.select(Post).filter_by(user_id=user_id)).scalars()
    posts = []
    for post in user_posts:
        posts.append({
            "id": post.id,
            "user_id": post.user_id,
            "photo": post.photo,
            "description": post.caption,
            "created_on": post.created_on,
        })
    return jsonify(posts=posts), 200


@app.route('/api/users/<user_id>/follow', methods=['POST', 'GET'])
@login_required
@requires_auth
def follow(user_id):
    if request.method == 'POST':
        """Create a Follow relationship between the current user and the target user."""
        follow = Follow(user_id=user_id, follower_id=int(current_user.get_id()))
        db.session.add(follow)
        db.session.commit()
        return jsonify({
            "message": "You are now following that user."
        }), 201
    if request.method == 'GET':
        follows = db.session.execute(db.select(Follow).filter_by(user_id=user_id)).scalars()
        return jsonify({
            "followers": len([follow for follow in follows])
        }), 201


@app.route('/api/v1/posts', methods=['GET'])
@login_required
@requires_auth
def get_all_posts():
    """Return all posts for all users"""
    posts = db.session.execute(db.select(Post)).scalars()
    all_posts = []
    for post in posts:
        likes = db.session.execute(db.select(Like).filter_by(id=post.id)).scalars()
        user = db.session.execute(db.select(User).filter_by(id=post.user_id)).scalar()
        all_posts.append({
            "id": post.id,
            "user_id": post.user_id,
            "username": user.username,
            "photo": url_for("getImage", filename=post.photo),
            "caption": post.caption,
            "created_on": post.created_on,
            "likes": len([like for like in likes])
        })
    return jsonify(all_posts), 200



@app.route('/api/v1/posts/<post_id>/like', methods=['POST'])
@login_required
@requires_auth
def like(post_id):
    """Set a like on the current Post by the logged in User"""
    post = db.session.execute(db.select(Post).filter_by(id=post_id)).scalar()
    if post is not None:
        likes = db.session.execute(db.select(Like).filter_by(post_id=post.id)).scalars()
        if post is not None:
            uid = int(current_user.get_id())
            like = Like(post_id, uid)
            db.session.add(like)
            db.session.commit()
            return jsonify({
                "message": "Post liked!",
                "likes": len([like for like in likes]) + 1
            }), 201


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


def generate_token(uid):
    timestamp = datetime.utcnow()
    payload = {
        "subject": uid,
        "iat": timestamp,
        "exp": timestamp + timedelta(minutes=60)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token


@app.route("/api/v1/images/<path:filename>")
def getImage(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)


@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).filter_by(id=user_id)).scalar()


@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})