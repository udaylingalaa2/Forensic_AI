import cv2
import numpy as np
import os
from PIL import Image, ImageChops

def analyze_noise_ela(filepath):
    """
    1. Performs Error Level Analysis (ELA).
    2. Calculates noise variance.
    """
    try:
        # --- ELA ANALYSIS ---
        original = Image.open(filepath).convert('RGB')
        
        # Save temp compressed version
        temp_path = filepath + ".tmp.jpg"
        original.save(temp_path, 'JPEG', quality=90)
        compressed = Image.open(temp_path)
        
        # Calculate difference
        diff = ImageChops.difference(original, compressed)
        extrema = diff.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        scale = 255.0 / max_diff if max_diff > 0 else 1
        diff = ImageChops.multiply(diff, scale)
        
        # Convert diff to array to measure intensity
        diff_data = np.array(diff)
        mean_diff = np.mean(diff_data)
        
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        # --- NOISE ANALYSIS (Laplacian) ---
        img_cv = cv2.imread(filepath)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Heuristics (Tweak these based on your data)
        ela_label = "LOW"
        if mean_diff > 15: ela_label = "HIGH"
        elif mean_diff > 8: ela_label = "MEDIUM"
        
        pattern_type = "ORGANIC" if laplacian_var > 100 else "SYNTHETIC"

        return {
            "ela_label": ela_label,
            "details": {
                "label": "Analysis Complete",
                "mean": f"{mean_diff:.4f}",
                "std": f"{np.std(diff_data):.4f}",
                "lap": f"{laplacian_var:.2f}",
                "pattern": pattern_type
            }
        }

    except Exception as e:
        print(f"Noise Error: {e}")
        return {
            "ela_label": "LOW",
            "details": {
                "label": "Error",
                "mean": "0", "std": "0", "lap": "0", "pattern": "UNKNOWN"
            }
        }