from flask import Blueprint, render_template, request, jsonify, session
from app import get_db
from app.tool import Tool

home_blueprint = Blueprint("home_blueprint", __name__, static_folder="../../static", template_folder="../../templates")


@home_blueprint.route("/")
def home():
    user_profile = None

    try:
        current_user = session["user_profile"]
    except KeyError:
        user_profile = None
        session.clear()
    else:
        db = get_db()
        user_profile = db.users.find_one({ "profile_id": current_user["id"]})
    
    return render_template("index.html", current_user=user_profile)


@home_blueprint.route("/", methods=["POST"])
def display_results():
    try:
        # the uploaded image has to be saved before PIL can open it
        uploaded_file = request.files['file']

    except KeyError:
        # no file was passed
        return jsonify("'file' required"), 400

    else:
        if uploaded_file == "" or uploaded_file.filename == "":
            return jsonify("No file passed"), 400

        extract_tool = Tool(uploaded_file)
        extract_tool.get_results()

        return jsonify({"results": extract_tool.computed_results}), 200  # sending back the computed results


home_blueprint.add_url_rule("/", view_func=home)
