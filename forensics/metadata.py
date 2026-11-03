from PIL import Image, ExifTags, UnidentifiedImageError


def analyze_metadata(filepath):
    """Check for camera metadata; metadata absence is a weak indicator only."""
    try:
        with Image.open(filepath) as image:
            exif_data = image.getexif()

        if not exif_data:
            return {"score_label": "HIGH", "desc": "No EXIF metadata found; this alone does not establish image origin."}

        names = {ExifTags.TAGS.get(tag_id, tag_id) for tag_id in exif_data}
        if "Make" in names and "Model" in names:
            return {"score_label": "LOW", "desc": "Camera make and model metadata found; metadata can be edited."}
        return {"score_label": "MEDIUM", "desc": "Partial EXIF metadata found; this is not proof of image origin."}
    except (OSError, UnidentifiedImageError, ValueError):
        return {"score_label": "INCONCLUSIVE", "desc": "Metadata could not be analyzed."}
