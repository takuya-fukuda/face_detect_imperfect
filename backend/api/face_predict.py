import os
import shutil
import base64
from pathlib import Path
from flask import jsonify
from .preprocess import load_image, extension_split, heic_convert, filename_convert
# from .paddleocr_predict import OCRProcessor
from api.facerecognition.face_recognition import face_similarity
from .error import handle_error
import logging
from dotenv import load_dotenv
load_dotenv()

import time

basedir = Path(__file__).parent.parent
logger = logging.getLogger(__name__)

def face_predict(request):
    try:
        file1 = request.files.get("file1")
        file2 = request.files.get("file2")

        if not file1 or not file2:
            return jsonify({"error": "2つのファイルが必要です"}), 400
        
        filename = file1.filename
        filename2 = file2.filename

        img_path = str(basedir / "data" / "input" /filename)
        img_path2 = str(basedir / "data" / "input" /filename2)
        file1.save(img_path)
        file2.save(img_path2)

        '''推論'''
        res = face_similarity(img_path, img_path2)

        print(res)
        # ファイルの処理
        # return jsonify({"result": "OK", "image": base64_encoded_image, ...})
        return jsonify({"message": res})
    
    except Exception as e:
        logger.error("想定外のエラー："+str(e))
        return jsonify({"message": "想定外のエラー："})
    
    finally:
        #元画像の削除
        if img_path and os.path.exists(img_path):
            os.remove(img_path)
        #元画像の削除
        if img_path2 and os.path.exists(img_path2):
            os.remove(img_path2)


