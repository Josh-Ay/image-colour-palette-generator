from flask import Blueprint, render_template
from markupsafe import escape
from app.custom_decorators.custom_decorators import login_required, admin_only

users_blueprint = Blueprint("users_blueprint", __name__, static_folder="../../static", template_folder="../../templates")


@users_blueprint.route("/<int:user_id>")
# @login_required
def get_user_profile(user_id):
    return render_template("user_page.html", current_user=escape(user_id))


@users_blueprint.route("/a/all")
# @login_required
# @admin_only
def show_all_users():
    return render_template("bbbootstrap-snippet.html")
