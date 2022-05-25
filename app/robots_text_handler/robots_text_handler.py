from app.robots_text_handler import robots_text_blueprint
from flask import send_from_directory, request


@robots_text_blueprint.route("/robots.txt")
def show_robots_text():
    return send_from_directory(robots_text_blueprint.static_folder, request.path[1:])
