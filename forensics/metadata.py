from PIL import Image, ExifTags

def analyze_metadata(filepath):
    """
    Checks for presence of EXIF data.
    AI images typically lack EXIF or have very little.
    """
    try:
        img = Image.open(filepath)
        exif_data = img._getexif()
        
        if not exif_data:
            return {"score_label": "HIGH", "desc": "No Metadata found."}
        
        # Check for specific camera tags (Make/Model)
        has_make = False
        has_model = False
        
        # Invert ExifTags for easy lookup
        tags = {v: k for k, v in ExifTags.TAGS.items()}
        
        for tag_id, value in exif_data.items():
            tag_name = ExifTags.TAGS.get(tag_id, tag_id)
            if tag_name == 'Make': has_make = True
            if tag_name == 'Model': has_model = True

        if has_make and has_model:
            return {"score_label": "LOW", "desc": "Camera Make/Model found."}
        else:
            return {"score_label": "MEDIUM", "desc": "Partial metadata found."}

    except Exception:
        return {"score_label": "HIGH", "desc": "Error reading metadata."}