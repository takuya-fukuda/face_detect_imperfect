import json
import base64
import re
from . import imperfect_predict, face_predict, face_register

from flask import Blueprint, jsonify, request

api = Blueprint("api", __name__)

#接続確認用アプリケーションルート
@api.route('/')
def index():
    return "test"

#マスク検出
@api.route('/image', methods=["POST"])
def imperfect():
    return imperfect_predict.imperfect_predict(request)

#顔認証類似度計測
@api.route('/face', methods=["POST"])
def face():
    return face_predict.face_predict(request)

#顔特徴量登録
@api.route('/face/register', methods=["POST"])
def register():
    return face_register.face_register(request)