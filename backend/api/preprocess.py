from pathlib import Path
from flask import jsonify
import PIL
import os
from os.path import splitext
import pillow_heif
from PIL import Image
import uuid
import logging

basedir = Path(__file__).parent.parent
logger = logging.getLogger(__name__)

def load_image(file):
    try:
        """画像の読み込み"""       
        # ファイルが空かどうかのチェック
        if file.filename == '' or file is None:
            return None, None

        filename = file.filename
        img_path = str(basedir / "data" / "input" /filename)
        file.save(img_path)

        return img_path, filename
    except Exception as e:
        raise(e)

def extension_split(img_path):
    ext = splitext(img_path)[1]
    return ext

def heic_convert(img_path):
    save_path = splitext(img_path)[0] + ".jpg"
    heif_file = pillow_heif.read_heif(img_path)
    for img in heif_file: 
        image = Image.frombytes(
            img.mode,
            img.size,
            img.data,
            'raw',
            img.mode,
            img.stride,
        )
    image.save(save_path, "JPEG")
    os.remove(img_path)

    return save_path

def filename_convert(img_path):
    ext = splitext(img_path)[1]
    directory_path = os.path.dirname(img_path)
    uniqid = uuid.uuid4()
    new_filename = os.path.join(directory_path, str(uniqid) + ext)

    # ファイルを新しい名前で上書きする（リネーム）
    os.rename(img_path, new_filename)

    return new_filename

def preprocess_default(file):
    try:
        if file.filename == '' or file is None:
            return None, None
        filename = file.filename
        img_path = str(basedir / "data" / "input" /filename)
        file.save(img_path)

        # ファイルのロードに失敗した場合の処理
        if img_path is None:
            logger.error("ファイルが空です")
            return jsonify({"message": 'ファイルが空です'}), 400

        # ファイル名チェック
        if filename == '' or filename is None:
            logger.error("ファイル名が空です")
            return jsonify({"message": 'ファイル名が空です'}), 400
        
        #拡張子チェック
        ext = extension_split(img_path)
        logger.info("拡張子:" + ext)
        if ext.lower() not in [".jpeg", ".jpg", ".png", ".heic"]:
            logger.error('AIがファイル拡張子に対応していません')
            return jsonify({"message": 'AIがファイル拡張子に対応していません'}), 400
        
        #拡張子チェック
        ext = extension_split(img_path)
        logger.info("拡張子:" + ext)
        if ext.lower() not in [".jpeg", ".jpg", ".png", ".heic"]:
            logger.error('AIがファイル拡張子に対応していません')
            return jsonify({"message": 'AIがファイル拡張子に対応していません'}), 400        

        #HEICのJPEG変換
        if ext == ".HEIC":
            img_path = heic_convert(img_path)
            logger.info("from heic to jpeg:" + img_path)

        #ファイル名の変更と上書き
        img_path = filename_convert(img_path)
        logger.info("file rename " + img_path)        

        return img_path, filename

    except Exception as e:
        raise(e)





    
