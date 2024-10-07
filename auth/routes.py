"""The app routes"""
import logging
import redis

from flask import render_template, Flask, request, flash, redirect, url_for
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    current_user,
    logout_user,
)

# For proxies
from werkzeug.middleware.proxy_fix import ProxyFix

# User Class
from auth.user import User

# Global/Enivironment variables
app = Flask(__name__)
logger = logging.getLogger('auth')
login_manager = LoginManager()
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Login-Manager init
login_manager.login_view = "login_page"
login_manager.login_message = "Hey there, To protect your account please re-enter your information."
login_manager.login_message_category = "info"
login_manager.refresh_view = "accounts.reauthenticate"
login_manager.needs_refresh_message = (
    "To protect your account, please reauthenticate to access this page."
)
login_manager.needs_refresh_message_category = "info"
login_manager.session_protection = "strong"


# For proxies
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


@app.get("/")
def index():
    """The root html response
    """
    logger.info(
        'Client %s connected to %s using method %s',
        request.remote_addr,
        request.path,
        request.method
    )
    return render_template("login.html")


@app.get("/")
def login_page():
    """The root html response
    """
    logger.info(
        'Client %s connected to %s using method %s',
        request.remote_addr,
        request.path,
        request.method
    )
    return render_template("login.html")


@app.get("/signup")
def signup():
    """The root html response
    """
    logger.info(
        'Client %s connected to %s using method %s',
        request.remote_addr,
        request.path,
        request.method
    )
    return render_template("signup.html")

@app.get('/account')
def account():
    """Account data page"""
    logger.info(
        'Client %s connected to %s using method %s',
        request.remote_addr,
        request.path,
        request.method
    )
    return render_template('account.html', current_user=current_user)

@app.get('/logout')
@login_required
def logout():
    """Logout User"""
    logger.info(
        'Client %s connected to %s using method %s',
        request.remote_addr,
        request.path,
        request.method
    )
    logout_user()
    next_arg = request.args.get('next')
    return redirect(next_arg), 200


@app.post("/create_user")
def create_user():
    """The create user response
    """
    logger.info(
        'Client %s connected to %s using method %s',
        request.remote_addr,
        request.path,
        request.method
    )
    if 'name' in request.form and 'email' in request.form and\
          'username' in request.form and 'password' in request.form:
        # New User
        new_user = User(
            name = request.form['name'],
            email = request.form['email'],
            username = request.form['username'],
            password = request.form['password'],
        )

        # Next redirect
        next_arg = request.args.get('next')

        # Checks if user exists
        if r.sismember('usernames', new_user.username) == 1 or \
        r.sismember('emails', new_user.email) == 1:
            flash('User already exsists', category="error")
            return redirect(url_for('signup')), 400

        # Added user to redis
        r.hset('users', mapping = new_user.serialize())

        r.sadd('usernames', new_user.username)
        r.sadd('emails', new_user.email)

        # Logs in user
        login_user(new_user)

        return redirect(next_arg), 201


@app.post('/login')
def login():
    """Logs in user"""
    logger.info(
        'Client %s connected to %s using method %s',
        request.remote_addr,
        request.path,
        request.method
    )
    if 'name' in request.form and 'email' in request.form and\
          'username' in request.form and 'password' in request.form:
        # New User

        user = User(
            name = request.form['name'],
            email = request.form['email'],
            username = request.form['username'],
            password = request.form['password'],
        )

        # Login user
        login_user(user)

        # Sends user to next page
        next_arg = request.args.get('next')
        return redirect(next_arg)
