from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
from PIL import Image
import numpy as np
from rgb_to_hex_converter import convert_to_hex
from collections import Counter
import os

load_dotenv()   # load the variables stored in the .env file

app = Flask(__name__, static_folder="static")
app.secret_key = os.environ.get("SECRET_KEY")
Bootstrap(app)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/", methods=["POST"])
def display_results():
    uploaded_file = request.files['file']   # getting the uploaded file
    if uploaded_file != "":
        uploaded_file.save(uploaded_file.filename)  # the uploaded image has to be saved before PIL can open it

        # creating a numpy array from the uploaded image opened by PIL
        img_arr = np.array(Image.open(uploaded_file.filename))

        img_hex_codes = []

        # getting the rgb values and converting to hex e.g rgb(0, 15, 10) == #000f0a
        for row in img_arr:
            for color_row in row:
                # 'color_row' below returns an array with the rgb values like so: [10 15 10]
                hex_code = convert_to_hex(color_row[0], color_row[1], color_row[2])
                img_hex_codes.append(hex_code)

        total_colors = len(img_hex_codes)   # the total number of colors present in the image

        counter = Counter(img_hex_codes)    # get the count of all the colors
        top_10_colors_list = counter.most_common(10)    # returns the most common 10 as a list as so: [('#hex_code', count), ('#hex_code', count), ....]

        computed_results = []
        result = {}

        for color_occurrence in top_10_colors_list:
            color_hex, count = color_occurrence
            percentage_occurrence = round((count / total_colors), 6)
            result["color_code"], result["percent_count"] = color_hex, percentage_occurrence

            computed_results.append(result)
            result = {}

        os.remove(uploaded_file.filename)   # deleting the uploaded image
        return jsonify({"results": computed_results}), 200  # sending back the computed results


@app.route("/robots.txt")
def show_robots_text():
    return send_from_directory(app.static_folder, request.path[1:])


if __name__ == "__main__":
    app.run()
