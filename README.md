# ForensicAI

ForensicAI is a Flask image-authenticity web app that combines a trained CNN model, EXIF metadata checks, and ELA/noise heuristics to estimate whether an uploaded image is likely AI-generated or real.

## Features
- Upload an image from the browser
- Run a TensorFlow CNN classifier
- Check EXIF metadata for camera signatures
- Run ELA and Laplacian-noise heuristics
- Display a verdict with a confidence-style score
- Keep analysis outputs cautious and labeled as inconclusive when the evidence is weak or unavailable

## Project structure
```text
Forensic_AI/
├── app.py                    # Flask app and request handling
├── requirements.txt         # Python dependencies
├── train_advanced_model.py   # CNN training script
├── .gitignore                # Local-data and secret exclusions
├── README.md                 # Project overview and usage
├── forensics/
│   ├── __init__.py
│   ├── metadata.py          # EXIF metadata analysis
│   └── noise_analysis.py    # ELA and noise analysis
├── static/
│   ├── uploads/             # Temporary uploaded files are stored here
│   └── css/
├── templates/
│   └── index.html            # Web interface
└── dataset/                  # Local dataset folder; not committed
```

## Requirements
- Python 3.10+
- Virtual environment recommended
- TensorFlow
- Flask
- NumPy
- Pillow
- OpenCV
- scikit-learn

## Setup
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Prepare the dataset
Create the dataset folder locally before training:
```text
Forensic_AI/
└── dataset/
    ├── ai_images/
    └── real_images/
```

Then train the CNN:
```bash
python train_advanced_model.py
```

The script saves the model to:
```text
model/ai_vs_real_model.h5
```

## Run the app
```bash
python app.py
```

Open the app in your browser at:
```text
http://127.0.0.1:5000
```

## Important notes
- The dataset and model are intentionally excluded from version control.
- Model output is binary and should be interpreted carefully.
- Scores are not forensic proof; they are heuristic indicators and should be treated as preliminary findings.
- The app uses a conservative verdict band and will return an inconclusive result when analysis cannot run reliably.

## Typical next improvements
- Add CI tests
- Add model validation metrics
- Add a proper production deployment configuration
- Add a downloadable forensic report
- Add support for video analysis and additional image-forensics features
