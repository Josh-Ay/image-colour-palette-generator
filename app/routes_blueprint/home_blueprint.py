from cgi import test
from flask import Blueprint, render_template, request, jsonify
from PIL import Image
import numpy as np
from rgb_to_hex_converter import convert_to_hex
from collections import Counter
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from arrayChunker import chunk_array

home_blueprint = Blueprint("home_blueprint", __name__, static_folder="../../static", template_folder="../../templates")


@home_blueprint.route("/")
def home():
    return render_template("index.html")


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

        img_arr, img_hex_codes, img_is_svg = [], [], False

        # the uploaded image has to be saved before PIL can open it/svglib can process it
        uploaded_file.save(uploaded_file.filename)

        # PIL cannot open svgs so it has to be converted to a png before proceeding
        if uploaded_file.filename.split(".")[1].lower() == "svg":
            img_is_svg = True
            png_file = svg2rlg(uploaded_file.filename)
            renderPM.drawToFile(png_file, uploaded_file.filename.split(".")[0] + ".png", fmt="PNG")

        if img_is_svg:
            img_arr = np.array(Image.open(uploaded_file.filename.split(".")[0] + ".png"))
        else:
            # opening up the uploaded using PIL
            img_arr = np.array(Image.open(uploaded_file.filename))

        # gives a len of 2 for gifs
        if len(np.shape(img_arr)) == 2:
            # getting the rgb values and converting to hex e.g rgb(0, 15, 10) == #000f0a
            img_hex_codes = [convert_to_hex(color_row[0], color_row[1], color_row[2]) for row in img_arr for color_row
                             in chunk_array(row, 3)]

        else:
            # getting the rgb values and converting to hex e.g rgb(0, 15, 10) == #000f0a
            img_hex_codes = [convert_to_hex(color_row[0], color_row[1], color_row[2]) for row in img_arr for color_row
                             in
                             row]  # 'color_row' returns an array with the rgb values like so: [10 15 10]

        # getting the count of all the colors present in the image
        counter = Counter(img_hex_codes)
        top_10_colors_list = counter.most_common(10)

        computed_results, result = [], {}

        for color_occurrence in top_10_colors_list:
            color_hex, count = color_occurrence
            percentage_occurrence = round((count / len(img_hex_codes)), 6)
            result["color_code"], result["percent_count"] = color_hex, percentage_occurrence

            computed_results.append(result)
            result = {}

        # deleting the uploaded image to save space on the server
        if img_is_svg:
            os.remove(uploaded_file.filename.split(".")[0] + ".png")

        os.remove(uploaded_file.filename)

        return jsonify({"results": computed_results}), 200  # sending back the computed results


home_blueprint.add_url_rule("/", view_func=home)
