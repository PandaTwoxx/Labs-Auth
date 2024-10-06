"""The app routes"""
import logging

from flask import render_template, Flask, request

# For proxies
from werkzeug.middleware.proxy_fix import ProxyFix


# Global/Enivironment variables
app = Flask(__name__)
logger = logging.getLogger('auth')


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
