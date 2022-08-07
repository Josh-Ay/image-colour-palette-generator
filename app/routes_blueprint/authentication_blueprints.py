from flask import Blueprint, render_template, request, url_for, session, redirect
from app import get_db, oauth
from app.routes_blueprint.registered_clients import registered_clients
from markupsafe import escape

authentication_blueprint = Blueprint("authentication_blueprint", __name__, static_folder="../../static", template_folder="../../templates")


@authentication_blueprint.route("/auth/<auth_type>", methods=["GET", "POST"])
def authenticate(auth_type):
    if request.method == "POST":

        if auth_type not in registered_clients:
            return render_template("404_page.html"), 404
        else:
            oauth_client = oauth.create_client(auth_type)
            return oauth_client.authorize_redirect(url_for("authentication_blueprint.authorize", client=auth_type, _external=True))

    if escape(auth_type) == "register":
        return render_template("login.html", card_title="Register", card_message="Welcome!", reroute_to="authentication_blueprint.authenticate", auth_type="login")
    elif escape(auth_type) == "login":
        return render_template("login.html", card_title="Login", card_message="Welcome back!", reroute_to="authentication_blueprint.authenticate", auth_type="register")

    return render_template("404_page.html"), 404


@authentication_blueprint.route("/authorize/<client>")
def authorize(client):

    if escape(client) not in registered_clients:
        return render_template("404_page.html"), 404

    oauth_client = oauth.create_client(escape(client))
    token = oauth_client.authorize_access_token()
    resp = oauth_client.get(registered_clients[escape(client)]["profile_key"], token=token)
    resp.raise_for_status()
    profile = resp.json()

    db = get_db()
    existing_user = db.users.find_one({ "profile_id": profile["id"]})

    if existing_user is None:
        # google
        if client == list(registered_clients.keys())[0]:
            db.users.insert_one({
                "profile_id": profile["id"],
                "profile_img": profile["picture"],
                "display_name": profile["name"],
            })
        # github
        else:
            db.users.insert_one({
                "profile_id": profile["id"],
                "profile_img": profile["avatar_url"],
                "display_name": profile["login"],
            })

    session["user_profile"] = profile
    session.permanent = True

    return redirect(url_for("users_blueprint.user_profile"))
