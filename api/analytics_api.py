
from flask import Blueprint, jsonify
import pandas as pd
import os
from src.history_logger import log_activity
analytics_bp = Blueprint(
    "analytics",
    __name__
)


@analytics_bp.route("/analytics", methods=["GET"])
def analytics():

    try:

        file_path = "datasets/cleaneddata/athena_cleaned.csv"

        if not os.path.exists(file_path):

            return jsonify({

                "status": "error",

                "message": "Cleaned dataset not found."

            }), 404

        df = pd.read_csv(file_path)

        webcam = df[df["Source"] == "webcam"]
        image = df[df["Source"] == "image"]

        response = {

            "status": "success",

            "message": "Analytics generated successfully.",

            "data": {

                "webcam": {

                    "records": int(webcam["People_Count"].count()),

                    "average": float(round(webcam["People_Count"].mean(), 2))
                    if not webcam.empty else 0,

                    "maximum": int(webcam["People_Count"].max())
                    if not webcam.empty else 0,

                    "minimum": int(webcam["People_Count"].min())
                    if not webcam.empty else 0

                },

                "image": {

                    "records": int(image["People_Count"].count()),

                    "average": float(round(image["People_Count"].mean(), 2))
                    if not image.empty else 0,

                    "maximum": int(image["People_Count"].max())
                    if not image.empty else 0,

                    "minimum": int(image["People_Count"].min())
                    if not image.empty else 0

                }

            }

        }
        
        log_activity(

    module="Insights",

    source="Analytics",

    people=0,

    status="Viewed"

)

        return jsonify(response), 200

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500
