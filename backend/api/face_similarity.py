import os
from pathlib import Path
from flask import request, jsonify
from sqlalchemy import select
from .preprocess import preprocess_default
from api.facerecognition.face_recognition import FaceRecognizer
from werkzeug.utils import secure_filename
from api.models import db, FaceEmbedding
import logging

basedir = Path(__file__).parent.parent
logger = logging.getLogger(__name__)
recognizer = FaceRecognizer()

def face_similarity(request):
    try:
        '''前処理'''
        file = request.files.get("file")
        #user_id = "test"
        username = request.form.get("username")
        if not file:
            return jsonify({"error": "画像ファイルとuser_idは必須です"}), 400
        img_path, filename = preprocess_default(file)

        '''推論'''
        embedding_tensor = recognizer.get_feature(img_path)
        embedding_list = embedding_tensor.squeeze().tolist()  # ベクトル(512次元)をリストに変換

        # --- 類似度検索 ---
        distance_col = FaceEmbedding.embedding.cosine_distance(embedding_list)

        # コサイン類似度を 1 - distance で計算 :contentReference[oaicite:1]{index=1}
        similarity_col = (1 - distance_col).label('similarity')

        # 距離（＝1-類似度）が小さい順、つまり類似度が高い順にソートして上位1件を取得
        stmt = (
            select(
                FaceEmbedding.username,
                similarity_col
            )
            .where(FaceEmbedding.username== username)  # ユーザIDでフィルタリング
            .order_by(distance_col)                   # 距離（1-類似度）が小さい順
            .limit(1)                                 # 上位1件のみ
        )
        result = db.session.execute(stmt).first()

        if result is None:
            return jsonify({"message": "該当ユーザのデータが見つかりません"}), 404

        # --- レスポンス整形 ---
        # record_id, sim = result.id, float(result.similarity)
        sim = float(result.similarity)
        return jsonify({
            "username": username,
            "similarity": sim
        }), 200

    except Exception as e:
        logger.error("例外のエラー："+str(e))
        return jsonify({"message": "例外エラーの発生"}), 400
    
    finally:
        #インプットイメージの削除
        if img_path and os.path.exists(img_path):
            os.remove(img_path)