from flask import Blueprint

robots_text_blueprint = Blueprint("robots_text_blueprint", __name__, static_folder="../../static",
                                  template_folder="../../templates")
