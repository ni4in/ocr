import numpy as np
import cv2
import base64
import json
from flask import Flask, request
from paddleocr import PaddleOCR

OCR_ENGINE = PaddleOCR(
    det_model_dir="ocr_models/ch_PP-OCRv4_det_infer", 
    rec_model_dir="ocr_models/ch_PP-OCRv4_rec_infer",
    cls_model_dir="ocr_models/ch_ppocr_mobile_v2.0_cls_infer",
    rec_char_dict_path="ocr_models/ppocr_keys_v1.txt",
    use_angle_cls=True,
    lang="en",
    det_db_box_thresh=0.4,
    drop_score=0.3,
)
app = Flask(__name__)


@app.route("/extract_text", methods=["POST", "GET"])
def extract_text():
    if request.method == "POST":
        image_b64 = request.form.get("image")
    else:
        image_b64 = request.args.get("image")
    image_np = np.frombuffer(base64.b64decode(image_b64), np.uint8)
    image_np = cv2.imdecode(image_np, flags=cv2.IMREAD_COLOR)
    results = OCR_ENGINE.ocr(image_np, cls=True)
    json_arr = []
    for result in results:
        output_arr = []
        for line in result:
            output = dict()
            output["bbox"] = line[0]
            output["text"] = line[1][0]
            output["score"] = line[1][1]
            output_arr.append(output)
        json_arr.extend(output_arr)
    return json.dumps(json_arr)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5544, debug=True)
