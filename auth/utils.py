"""Utility Functions"""

from http import HTTPStatus
from flask import abort, request, redirect, url_for
from service.routes import login_manager, r



@login_manager.unauthorized_handler
def unauthorized():
    """Endpoint for unauthorized
    Returns:
        Response: redirects to login page, http code 200
        NoReturn: aborts with unauthorized status
    """
    if request.blueprint == "api":
        abort(HTTPStatus.UNAUTHORIZED)
    return redirect(url_for("login_page")), 200


@login_manager.user_loader
def user_loader(user_id):
    """Returns user object

    Args:
        user_id (str): The id of the user

    Returns:
        User: The loaded user object
    """
    return r.hget('users', user_id)
