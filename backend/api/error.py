import os
from flask import jsonify

def handle_error(message, img_path, result_save_path):
    #input画像の削除
    if img_path and os.path.exists(img_path):
        os.remove(img_path)
    #result画像の削除
    if result_save_path and os.path.exists(result_save_path):
        os.remove(result_save_path)

    return jsonify({"message": message})

class AppError(Exception):
    def __init__(self, message: str, stt: int, http_status: int = 400):
        super().__init__(message)
        self.http_status = http_status
        self.message = message