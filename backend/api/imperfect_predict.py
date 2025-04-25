import os
import shutil
import base64
from pathlib import Path
from flask import jsonify
from .preprocess import preprocess_default
# from .paddleocr_predict import OCRProcessor
from api.facemask.facemask_predict import mask_judge
from api.facedetection.mp_face_detection import detect_faces
from .error import handle_error
import logging
from dotenv import load_dotenv
load_dotenv()

import time

basedir = Path(__file__).parent.parent
logger = logging.getLogger(__name__)

def imperfect_predict(request):
    img_path=None
    result_save_path=None

    '''前処理'''
    try:
        # 実行開始時間を記録
        start_time = time.time()

        #ファイル受け取り
        if 'file' not in request.files:
            return jsonify({"file": "None"})

        file = request.files['file']

        # 前処理
        img_path, filename = preprocess_default(file)

    except Exception as e:
        logger.error("前処理部分での想定外のエラー："+str(e))
        return handle_error("前処理部分での想定外のエラー", img_path, result_save_path), 400

    '''推論：MediaPipeとFaceMaskで推論'''
    try:
        mp_response = detect_faces(img_path)
        mask_response = mask_judge(img_path, filename)

     
    except Exception as e:
        logger.error("AI推論時の想定外のエラー："+str(e))
        return handle_error("AI推論時の想定外のエラー", img_path, result_save_path), 400

    '''後処理'''
    try:
        result_image_path = mp_response["output_path"]
        with open(result_image_path, "rb") as img_file:
            encoded_image = base64.b64encode(img_file.read()).decode('utf-8')

        result_data = {
            "image" : encoded_image,
            "mask" : "マスクの有無：" + mask_response["mask"],
            "face_count" : "検出された顔の数：" + str(mp_response["face_count"])
        }

        # 実行終了時間を記録
        end_time = time.time()

        # 経過時間を計算
        elapsed_time = end_time - start_time
        print(f"処理にかかった時間: {elapsed_time:.2f}秒")

        print(jsonify(result_data))

        return jsonify(result_data)

    except Exception as e:
        logger.error("AI推論後の後処理で想定外のエラー："+str(e))
        return handle_error("AI推論後の後処理で想定外のエラー：", img_path, result_save_path), 400

    finally:
        #インプットイメージの削除
        if img_path and os.path.exists(img_path):
            os.remove(img_path)

        #OCR結果イメージの削除
        if result_image_path and os.path.exists(result_image_path):
            os.remove(result_image_path)
