from app.error_handlers import error_blueprint
from flask import render_template, flash


@error_blueprint.errorhandler(404)
def handle_page_not_found(e):
    return render_template("404_page.html"), 404


@error_blueprint.errorhandler(403)
def handle_unauthorized_access(e):
    flash("You need to be logged in to view this page.")
    return render_template("login.html", card_title="Login", card_message="Welcome back!",
                           reroute_to="authentication_blueprint.authenticate",
                           auth_type="register"), 403
