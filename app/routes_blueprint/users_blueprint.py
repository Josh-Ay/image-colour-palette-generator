import json
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
import pymongo
from app import get_db
from app.custom_decorators.custom_decorators import login_required
import re

users_blueprint = Blueprint("users_blueprint", __name__, static_folder="../../static", template_folder="../../templates")


@users_blueprint.route("/user", methods=["GET", "POST"])
@login_required
def user_profile():
    logged_in_user = session["user_profile"]

    db = get_db()
    user_profile = db.users.find_one({ "profile_id": logged_in_user["id"]})
    user_saved_results = list(db.colors.find({ "owner": user_profile["profile_id"] }).sort("_id", pymongo.DESCENDING))
    all_colors = [{"light_color": True, "code": _["color_code"] } if bool(re.search(r"e{2,}|f{2,}", _["color_code"])) or _["color_code"].count("e") > 1 or _["color_code"].count("f") > 1 else {"light_color": False, "code": _["color_code"]} for result in user_saved_results for _ in json.loads(result["results"])]
    all_results = [{ 'result': json.loads(result["results"]), 'result_id': str(result["_id"]), 'created': str(result["_id"].generation_time) } for result in user_saved_results]

    if request.method == "POST":
        color_result = request.form.get("upload-result")
        db.colors.insert_one({
            "owner": user_profile["profile_id"],
            "results" : color_result,
        })

        flash("Successfully saved result!")

        return redirect(url_for("users_blueprint.user_profile"))

    return render_template("user_page.html", current_user=user_profile, recent_colors=all_colors[:12], all_colors=all_colors, all_results=all_results)


@users_blueprint.route("/logout")
def handle_logout():
    
    session.clear()
    
    return redirect(url_for("home_blueprint.home"))