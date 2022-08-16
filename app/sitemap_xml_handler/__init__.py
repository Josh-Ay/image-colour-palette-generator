from flask import Blueprint

sitemap_handler_blueprint = Blueprint("sitemap_handler_blueprint", __name__, static_folder="../../static",
                                  template_folder="../../templates")
