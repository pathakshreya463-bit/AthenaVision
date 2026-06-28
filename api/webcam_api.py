from flask import Blueprint, jsonify

from src.webcam_processor import analyze_webcam

webcam_bp = Blueprint(
    "webcam",
    __name__
)


@webcam_bp.route("/webcam")
def webcam():

    result = analyze_webcam()

    return jsonify(result)