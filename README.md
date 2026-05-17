# 🔍 Forensic AI — Can You Tell What's Real Anymore?

Hey! I built this because AI-generated images are getting so good that most people can't spot them anymore. ForensicAI is a web app that does one thing really well:

> **Upload any image → Get a verdict: Real ✅ or AI-Generated ❌**

It doesn't guess. It runs a proper forensic investigation — checking hidden file metadata, pixel compression patterns, and a deep learning model — all at once.

---

## ⚠️ Read This First

The **dataset** and **trained model** are not included in this repo. GitHub doesn't allow large files. You need to set them up yourself before running the app — it takes about 10 minutes and everything is completely free.

---

## 📥 Step 1 — Download the Dataset from Kaggle

The dataset used to train this model is **"AI vs Real Images"** on Kaggle.

👉 Click this link and hit Download:
```
https://www.kaggle.com/datasets/cashbowman/ai-generated-images-vs-real-images
```

> You need a free Kaggle account to download. Sign up at kaggle.com if you don't have one — it's free and takes 2 minutes.

---

## 📂 Step 2 — Set Up the Dataset Folder

After downloading, unzip the file. You'll find two folders inside — one with AI images and one with real photos.

Place them inside the project exactly like this:

```
Forensic_AI/
└── dataset/
    ├── ai_images/       ← all AI-generated images go here
    └── real_images/     ← all real photographs go here
```

> The `dataset/` folder is in `.gitignore` so it will never get pushed to GitHub by accident.

---

## 🏋️ Step 3 — Train the Model

Now run the training script:

```bash
python train_advanced_model.py
```

This will automatically:
- Load all images from your `dataset/` folder
- Train the EfficientNetB0 model on them
- Save the finished model as `model/forensic_model.h5`

How long will it take?

| Machine | Estimated Time |
|---|---|
| With a GPU (NVIDIA) | 15 – 30 minutes |
| CPU only | 1 – 3 hours |

Just let it run. When it finishes, the model file will appear in the `model/` folder automatically.

---

## 🚀 Step 4 — Run the Web App

Now that the model is trained, start the app:

**Clone the repo**
```bash
git clone https://github.com/udaylingalaa2/Forensic_AI.git
cd Forensic_AI
```

**Create a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

**Install dependencies**
```bash
pip install -r requirements.txt
```

**Start the app**
```bash
python app.py
```

**Open in your browser**
```
http://127.0.0.1:5000
```

Upload any image — real or AI-generated — and the system will analyse it in seconds.

---

## 🧠 How It Works

Three engines run on every image you upload:

**Engine 1 — The Detective 🕵️**
Reads the invisible metadata baked into the file (EXIF data). A real camera always leaves a fingerprint — camera model, GPS, compression type. AI images have none of that. They're too clean.

**Engine 2 — The Brain 🧬**
A deep learning model (EfficientNetB0) trained on thousands of real and AI images. It scans for microscopic artefacts that AI generators accidentally leave behind — invisible to the human eye, but not to the model.

**Engine 3 — The Guard 🛡️**
Logs the IP address of whoever uploaded the image and flags suspicious sources.

All three engines give their verdict. The final result is shown with a confidence percentage.

---

## 📁 Project Structure

```
Forensic_AI/
│
├── app.py                    ← Run this to start the web app
├── requirements.txt          ← Install these before anything else
├── train_advanced_model.py   ← Run this to train the model
│
├── dataset/                  ← You create this (see Step 2 above)
│   ├── ai_images/
│   └── real_images/
│
├── model/                    ← model.h5 gets saved here after training
├── templates/                ← HTML web pages
├── static/css/               ← Styling
└── forensics/                ← The forensic analysis logic
```

---

## ❓ Common Problems

**"Model file not found" error**
→ Training hasn't finished yet, or `train_advanced_model.py` didn't run successfully. Check the terminal for errors.

**"No such file or directory: dataset/"**
→ You haven't created the dataset folder yet. Go back to Step 2.

**Training is extremely slow**
→ Normal on CPU. If you have an NVIDIA GPU, install `tensorflow-gpu` instead of `tensorflow` for a big speed boost.

**Port 5000 already in use**
→ Open `app.py` and change the last line to `app.run(port=5001)` then open `http://127.0.0.1:5001` in your browser.

---

## 🔮 What I Want to Add Next

- [ ] Deploy online so anyone can use it without installing anything
- [ ] Generate a downloadable PDF forensics report
- [ ] Add deepfake face detection
- [ ] Video support — analyse frame by frame

---

## 🙋 About

Built by **Uday Kiran** — a student passionate about AI and cybersecurity.

This started as a simple question: *"Can I build something that fights AI misinformation?"*
Turns out — yes.

If this helped you or impressed you, a ⭐ star on GitHub would genuinely make my day!

[@udaylingalaa2](https://github.com/udaylingalaa2)
