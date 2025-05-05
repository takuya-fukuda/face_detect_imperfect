import json
import base64
import re
from . import imperfect_predict, face_register, two_face_predict, face_similarity

from flask import Blueprint, jsonify, request

api = Blueprint("api", __name__)

#接続確認用アプリケーションルート
@api.route('/')
def index():
    return "test"

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