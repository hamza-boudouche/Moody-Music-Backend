from app.moodrec import bp
from app.utils import Mood, recognition
from flask import request
import logging
from PIL import Image
import base64
import io
import numpy as np


@bp.route("/rec", methods=["POST"])
def getMood():
    # FIXME: verify if the max % is bigger than a certain threshold, else return sucess: False
    logging.info(f"request: POST /moodrec/rec - {request.get_json()}")
    content = request.get_json()
    pic_base64 = content.get("image")
    image_np = np.array(Image.open(io.BytesIO(base64.b64decode(pic_base64))))
    detected_mood = recognition.detectMood(image_np)
    return {"success": True, "detectedMood": detected_mood}
