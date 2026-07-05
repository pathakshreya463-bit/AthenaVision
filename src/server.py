from flask import Flask, jsonify

from api.analytics_api import analytics_bp
from api.image_api import image_bp
from api.webcam_api import webcam_bp

app = Flask(__name__)

# ----------------------------
# Register API Blueprints
# ----------------------------

app.register_blueprint(analytics_bp)
app.register_blueprint(image_bp)
app.register_blueprint(webcam_bp)


# ----------------------------
# Home Route
# ----------------------------

@app.route("/")
def home():

    return jsonify({

        "Project": "AthenaVision",
        "Version": "1.0",
        "Status": "Running"

    })


# ----------------------------
# Health Check
# ----------------------------

@app.route("/health")
def health():

    return jsonify({

        "Health": "OK"

    })


# ----------------------------
# Run Server
# ----------------------------

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True,

        use_reloader=False

    )