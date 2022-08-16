from app.sitemap_xml_handler import sitemap_handler_blueprint
from flask import send_from_directory, request


@sitemap_handler_blueprint.route("/sitemap_index.xml")
def sitemap_xml_handler():
    return send_from_directory(sitemap_handler_blueprint.static_folder, request.path[1:])
