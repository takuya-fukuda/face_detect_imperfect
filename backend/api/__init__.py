import json
import base64
import re
from . import imperfect_predict, face_register, two_face_predict, face_similarity
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import User


api = Blueprint("api", __name__)

#接続確認用アプリケーションルート
@api.route('/')
@jwt_required()  # ← ここでトークン必須を宣言
def index():
    return "test"

#認証用ルート
@api.route('/login', methods=["POST"])
def login():
    #data = request.get_json()
    username = request.form.get('username')
    password = request.form.get('password')

    # ユーザー名とパスワードの検証
    if not username or not password:
        return jsonify({"error": "Invalid username or password"}), 400
    
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid username or password"}), 401
    
    access_token = create_access_token(identity=str(user.id)) #Configで登録した有効期間と秘密鍵を使用する

    return jsonify({"access_token": access_token}), 200

#不備検出
@api.route('/image', methods=["POST"])
def imperfect():
    return imperfect_predict.imperfect_predict(request)

#2枚顔画像の類似度計測（DBなし）
@api.route('/twoface', methods=["POST"])
def twoface():
    return two_face_predict.two_face_predict(request)

#顔特徴量登録（DBあり）
@api.route('/face/register', methods=["POST"])
def register():
    return face_register.face_register(request)

#顔特類似度突合（DBあり）
@api.route('/face/similarity', methods=["POST"])
def similarity():
    return face_similarity.face_similarity(request)