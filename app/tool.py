import threading
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import os
from PIL import Image
import numpy as np
from rgb_to_hex_converter import convert_to_hex
from arrayChunker import chunk_array
from collections import Counter


class Tool:
    def __init__(self, uploaded_img_file):
        self.img_file = uploaded_img_file
        self.computed_results = []

    def get_results(self):
        new_result_thread = threading.Thread(target=self._extract_colors)
        new_result_thread.start()
        new_result_thread.join()

        print(f'Color extraction thread completed for: {self.img_file.filename}')
    
    def _extract_colors(self):
        
        img_arr, img_hex_codes, img_is_svg = [], [], False
        
        # the uploaded image has to be saved before PIL can open it/svglib can process it
        self.img_file.save(self.img_file.filename)

        # PIL cannot open svgs so it has to be converted to a png before proceeding
        if self.img_file.filename.split(".")[1].lower() == "svg":
            img_is_svg = True
            png_file = svg2rlg(self.img_file.filename)
            renderPM.drawToFile(png_file, self.img_file.filename.split(".")[0] + ".png", fmt="PNG")

        if img_is_svg:
            img_arr = np.array(Image.open(self.img_file.filename.split(".")[0] + ".png"))
        else:
            # opening up the uploaded using PIL
            img_arr = np.array(Image.open(self.img_file.filename))

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

        for color_occurrence in top_10_colors_list:
            result = {}

            color_hex, count = color_occurrence
            percentage_occurrence = round((count / len(img_hex_codes)), 6)
            result["color_code"], result["percent_count"] = color_hex, percentage_occurrence

            self.computed_results.append(result)

        # deleting the uploaded image to save space on the server
        if img_is_svg:
            os.remove(self.img_file.filename.split(".")[0] + ".png")

        os.remove(self.img_file.filename)
        print('Done extracting colors -> ', self.computed_results)
