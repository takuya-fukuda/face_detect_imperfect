import os
from pathlib import Path
from flask import jsonify
from .preprocess import preprocess_default
#from api.facerecognition.face_recognition import face_similarity
from api.facerecognition.face_recognition import FaceRecognizer
import logging
from dotenv import load_dotenv
load_dotenv()

basedir = Path(__file__).parent.parent
logger = logging.getLogger(__name__)

def face_predict(request):
    try:
        '''前処理'''
        file1 = request.files.get("file1")
        file2 = request.files.get("file2")

        if not file1 or not file2:
            return jsonify({"error": "2つのファイルが必要です"}), 400
        
        img_path, filename = preprocess_default(file1)
        img_path2, filename2 = preprocess_default(file2)

        '''推論'''
        #res = face_similarity(img_path, img_path2)
        facecheck = FaceRecognizer()
        res = facecheck.similarity(img_path, img_path2)

        print(res)

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


