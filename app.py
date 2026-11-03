import os
import tempfile

import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, render_template, request
from PIL import Image, UnidentifiedImageError
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img

from forensics.metadata import analyze_metadata
from forensics.noise_analysis import analyze_noise_ela

os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
MODEL_PATH = os.path.join(BASE_DIR, "model", "ai_vs_real_model.h5")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
MAX_UPLOAD_BYTES = 15 * 1024 * 1024
IMG_SIZE = (224, 224)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_BYTES
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

try:
    model = load_model(MODEL_PATH)
    print(f"Loaded image classifier from {MODEL_PATH}")
except (OSError, ValueError) as exc:
    print(f"Classifier unavailable ({exc}). Train the model before relying on CNN results.")
    model = None


def prepare_image(filepath):
    image = load_img(filepath, target_size=IMG_SIZE)
    array = img_to_array(image) / 255.0
    return np.expand_dims(array, axis=0)


def validate_image(filepath, extension):
    """Verify actual image contents instead of trusting the submitted filename."""
    try:
        with Image.open(filepath) as image:
            if image.format not in {"JPEG", "PNG", "WEBP", "BMP"}:
                raise ValueError("Unsupported image format. Upload JPG, PNG, WEBP, or BMP.")
            image.verify()
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        raise ValueError("The uploaded file is not a valid, safe image.") from exc


@app.errorhandler(413)
def upload_too_large(_error):
    return jsonify({"error": True, "message": "Image is too large. Maximum upload size is 15MB."}), 413


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    uploaded = request.files.get("file")
    if uploaded is None or not uploaded.filename:
        return jsonify({"error": True, "message": "Choose an image to upload."}), 400

    extension = os.path.splitext(uploaded.filename)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        return jsonify({"error": True, "message": "Unsupported file type. Upload JPG, PNG, WEBP, or BMP."}), 400

    filepath = None
    try:
        # Use a generated name, never the client-supplied filename, on the server.
        with tempfile.NamedTemporaryFile(
            mode="wb", suffix=extension, dir=app.config["UPLOAD_FOLDER"], delete=False
        ) as temp_file:
            filepath = temp_file.name
            uploaded.save(temp_file)

        if os.path.getsize(filepath) > MAX_UPLOAD_BYTES:
            return jsonify({"error": True, "message": "Image is too large. Maximum upload size is 15MB."}), 413

        validate_image(filepath, extension)
        metadata = analyze_metadata(filepath)
        noise = analyze_noise_ela(filepath)

        prediction_label = "Inconclusive"
        confidence = None
        ai_probability = None
        if model is not None:
            model_score = float(model.predict(prepare_image(filepath), verbose=0)[0][0])
            # flow_from_directory assigns ai_images=0 and real_images=1 alphabetically.
            ai_probability = 1.0 - model_score
            confidence = max(ai_probability, model_score)
            if ai_probability >= 0.60:
                prediction_label = "AI-Generated"
            elif ai_probability <= 0.40:
                prediction_label = "Real"

        return jsonify({
            "error": False,
            "prediction": prediction_label,
            "score": confidence,
            "ai_probability": ai_probability,
            "exif_score": metadata["score_label"],
            "exif_desc": metadata["desc"],
            "ela_score": noise["ela_label"],
            "noise_info": noise["details"],
            "disclaimer": "Automated indicators are not proof of image origin. Treat results as preliminary.",
        })
    except ValueError as exc:
        return jsonify({"error": True, "message": str(exc)}), 400
    except Exception:
        app.logger.exception("Image analysis failed")
        return jsonify({"error": True, "message": "Image analysis failed. Please try another image."}), 500
    finally:
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except OSError:
                app.logger.warning("Could not remove temporary upload %s", filepath)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG", "0").lower() in {"1", "true"},
    )
