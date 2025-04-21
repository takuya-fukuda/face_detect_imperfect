import os
import shutil
import base64
from pathlib import Path
from flask import jsonify
from .preprocess import load_image, extension_split, heic_convert, filename_convert
# from .paddleocr_predict import OCRProcessor
from api.facemask.facemask_predict import mask_judge
from .error import handle_error
import logging
from dotenv import load_dotenv
load_dotenv()

import time

basedir = Path(__file__).parent.parent
logger = logging.getLogger(__name__)

def mask_predict(request):
    '''前処理'''
    # 実行開始時間を記録
    start_time = time.time()
    
    img_path=None #Except部分でエラーが出るので初期化
    result_save_path=None #Except部分でエラーが出るので初期化
    try:
        #ファイルのロード
        img_path, filename = load_image(request)
        
        logger.info(img_path)

        # ファイルのロードに失敗した場合の処理
        if img_path is None:
            logger.error("ファイルが空です")
            return jsonify({"message": 'ファイルが空です', "race": "", "date": "", "sum": "", "uid": "", "image": ""}), 400

        # ファイル名チェック
        if filename == '' or filename is None:
            logger.error("ファイル名が空です")
            return jsonify({"message": 'ファイル名が空です', "race": "", "date": "", "sum": "", "uid": "", "image": ""}), 400
   
        #拡張子チェック
        ext = extension_split(img_path)
        logger.info("拡張子:" + ext)
        if ext.lower() not in [".jpeg", ".jpg", ".png", ".heic"]:
            logger.error('AIがファイル拡張子に対応していません')
            return jsonify({"message": 'AIがファイル拡張子に対応していません', "race": "", "date": "", "sum": "", "uid": "", "image": ""}), 400

        #HEICのJPEG変換
        if ext == ".HEIC":
            img_path = heic_convert(img_path)
            logger.info("from heic to jpeg:" + img_path)

        #ファイル名の変更と上書き
        img_path = filename_convert(img_path)
        logger.info("file rename " + img_path)

    except Exception as e:
        logger.error("前処理部分での想定外のエラー："+str(e))
        return handle_error("前処理部分での想定外のエラー", img_path, result_save_path), 400

    '''推論：PaddleOCRで推論'''
    try:
        response = mask_judge(img_path, filename)

     
    except Exception as e:
        logger.error("AI推論時の想定外のエラー："+str(e))
        return handle_error("AI推論時の想定外のエラー", img_path, result_save_path), 400

    '''後処理'''
    try:
        result_image_path = response["result_path"]
        with open(result_image_path, "rb") as img_file:
            encoded_image = base64.b64encode(img_file.read()).decode('utf-8')

        result_data = {
            "image" : encoded_image,
            "mask" : response["mask"]
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
