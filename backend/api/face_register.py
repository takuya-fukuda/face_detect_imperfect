import os
from pathlib import Path
from flask import request, jsonify
from .preprocess import preprocess_default
from api.facerecognition.face_recognition import FaceRecognizer
from werkzeug.utils import secure_filename
from api.models import db, FaceEmbedding
import logging

basedir = Path(__file__).parent.parent
logger = logging.getLogger(__name__)
recognizer = FaceRecognizer()

def face_register(request):
    try:
        '''前処理'''
        file = request.files.get("file")
        user_id = "test"
        if not file:
            return jsonify({"error": "画像ファイルとuser_idは必須です"}), 400
        img_path, filename = preprocess_default(file)

        '''推論'''
        embedding_tensor = recognizer.get_feature(img_path)
        embedding_list = embedding_tensor.squeeze().tolist()  # ベクトル(512次元)をリストに変換

        '''後処理'''
        #DB定義読み込み
        new_embedding = FaceEmbedding(user_id=user_id, embedding=embedding_list)
        db.session.add(new_embedding)
        db.session.commit()

        return jsonify({"message": "顔特徴量を登録しました"}), 201
    
    except Exception as e:
        logger.error("例外のエラー："+str(e))
        return jsonify({"message": "例外エラーの発生"}), 400
    
    finally:
        #インプットイメージの削除
        if img_path and os.path.exists(img_path):
            os.remove(img_path)

