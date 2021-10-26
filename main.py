from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
from PIL import Image
import numpy as np
from rgb_to_hex_converter import convert_to_hex
from collections import Counter
import os
from itertools import product

load_dotenv()   # load the variables stored in the .env file

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
Bootstrap(app)


@app.get("/")
def home():

    return render_template("index.html")


@app.post("/")
def display_results():
    uploaded_file = request.files['file']   # getting the uploaded file
    if uploaded_file != "":
        uploaded_file.save(uploaded_file.filename)  # the uploaded image has to be saved before PIL can open it

        # creating a numpy array from the uploaded image opened by PIL
        img_arr = np.array(Image.open(uploaded_file.filename))

        img_hex_codes = []

        # getting the rgb values and converting to hex e.g rgb(0, 15, 10) == #000f0a
        for row, column in product(range(img_arr.shape[0]), range(img_arr.shape[1])):   # the ideal way would be looping through each row then through colum but product() is faster than nested loops
            # 'img_arr[row][column]' below returns an array with the rgb values like so: [10 15 10]
            hex_code = convert_to_hex(img_arr[row][column][0], img_arr[row][column][1], img_arr[row][column][2])
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


if __name__ == "__main__":
    app.run()
