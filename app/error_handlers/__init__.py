from flask import Blueprint

error_blueprint = Blueprint("error_blueprint", __name__, static_folder="../../static", template_folder="../../templates")
