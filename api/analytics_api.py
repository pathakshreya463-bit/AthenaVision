from flask import Blueprint, jsonify
import pandas as pd

analytics_bp = Blueprint(
    "analytics",
    __name__
)

@analytics_bp.route("/analytics")
def analytics():

    df = pd.read_csv(
        "datasets/cleaneddata/athena_cleaned.csv"
    )

    webcam = df[df["Source"]=="webcam"]
    image = df[df["Source"]=="image"]

    response = {

        "webcam":{

            "records":int(webcam["People_Count"].count()),

            "average":float(round(webcam["People_Count"].mean(),2)),

            "maximum":int(webcam["People_Count"].max()),

            "minimum":int(webcam["People_Count"].min())

        },

        "image":{

            "records":int(image["People_Count"].count()),

            "average":float(round(image["People_Count"].mean(),2)),

            "maximum":int(image["People_Count"].max()),

            "minimum":int(image["People_Count"].min())

        }

    }

    return jsonify(response)