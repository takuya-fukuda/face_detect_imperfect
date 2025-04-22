import json
import base64
import re
from . import mask_predict, face_predict

from flask import Blueprint, jsonify, request

api = Blueprint("api", __name__)

#接続確認用アプリケーションルート
@api.route('/')
def index():
    return "test"

#マスク検出
@api.route('/image', methods=["POST"])
def mask():
    return mask_predict.mask_predict(request)

#顔認証類似度計測
@api.route('/face', methods=["POST"])
def face():
    return face_predict.face_predict(request)