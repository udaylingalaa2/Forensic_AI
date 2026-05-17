from flask import Flask, render_template, request, jsonify
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from werkzeug.utils import secure_filename

# Import custom forensic modules
from forensics.metadata import analyze_metadata
from forensics.noise_analysis import analyze_noise_ela

# ------------------------------------
# CONFIG
# ------------------------------------
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
MODEL_PATH = os.path.join(BASE_DIR, "model", "ai_vs_real_model.h5")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ------------------------------------
# LOAD MODEL
# ------------------------------------
print("🔍 Loading model...")
try:
    model = load_model(MODEL_PATH)
    print("✔ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    print("Make sure 'ai_vs_real_model.h5' is in the 'model' folder.")
    model = None

# ------------------------------------
# HELPERS
# ------------------------------------
IMG_SIZE = (224, 224)

def prepare_image(filepath):
    img = load_img(filepath, target_size=IMG_SIZE)
    img = img_to_array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# ------------------------------------
# ROUTES
# ------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": True, "message": "No file uploaded"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": True, "message": "Invalid file name"})

    # Save File
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        # 1. CNN Model Prediction
        if model:
            img_array = prepare_image(filepath)
            prediction = model.predict(img_array)[0][0]
            cnn_score = float(prediction)
            label = "AI-Generated" if cnn_score > 0.5 else "Real"
        else:
            # Fallback if model is missing
            cnn_score = 0.0
            label = "Model Missing"

        # 2. Forensic Analysis
        meta_result = analyze_metadata(filepath)
        noise_result = analyze_noise_ela(filepath)

        # 3. Cleanup (Optional: delete file after processing)
        # os.remove(filepath)

        return jsonify({
            "error": False,
            "filename": filename,
            "prediction": label,
            "score": cnn_score,
            "exif_score": meta_result['score_label'], # HIGH/MEDIUM/LOW
            "ela_score": noise_result['ela_label'],   # HIGH/MEDIUM/LOW
            "noise_info": noise_result['details']     # Dict of noise stats
        })

    except Exception as e:
        return jsonify({"error": True, "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)