
from flask import Blueprint, jsonify

from src.webcam_processor import analyze_webcam

webcam_bp = Blueprint(
    "webcam",
    __name__
)


@webcam_bp.route("/webcam", methods=["POST"])
def webcam():

    try:

        results = analyze_webcam()

        return jsonify({
            "status": "success",
            "message": "Webcam analysis completed successfully.",
            "data": results
        }), 200

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

