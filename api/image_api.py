from flask import Blueprint, jsonify

from src.image_processor import analyze_images

image_bp = Blueprint("image", __name__)


@image_bp.route("/image", methods=["POST"])
def image():

    try:

        results = analyze_images()

        return jsonify({
            "status": "success",
            "message": "Image analysis completed successfully.",
            "data": results
        }), 200

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500