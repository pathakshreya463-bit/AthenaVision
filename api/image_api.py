from flask import Blueprint, jsonify

from src.image_processor import analyze_images

image_bp = Blueprint(
    "image",
    __name__
)


@image_bp.route("/image")
def image():

    results = analyze_images()

    return jsonify(results)