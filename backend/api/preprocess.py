from pathlib import Path
from flask import jsonify
import PIL
import os
from os.path import splitext
import pillow_heif
from PIL import Image
import uuid
import logging
from .error import AppError

logger = logging.getLogger(__name__)


class PreProcess:
    def __init__(self):
        self.basedir = Path(__file__).parent.parent

    def __call__(self, request):
        return self.preprocess_default(request)

    def load_image(self, file):
        try:
            """画像の読み込み"""       
            # ファイルが空かどうかのチェック
            if file.filename == '' or file is None:
                return None, None

            filename = file.filename
            img_path = str(self.basedir / "data" / "input" /filename)
            file.save(img_path)

            return img_path, filename
        except Exception as e:
            raise(e)

    def extension_split(self, img_path):
        ext = splitext(img_path)[1]
        return ext

    def heic_convert(self, img_path):
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

    def filename_convert(self, img_path):
        ext = splitext(img_path)[1]
        directory_path = os.path.dirname(img_path)
        uniqid = uuid.uuid4()
        new_filename = os.path.join(directory_path, str(uniqid) + ext)

        # ファイルを新しい名前で上書きする（リネーム）
        os.rename(img_path, new_filename)

        return new_filename

    def preprocess_default(self, request):

        #ファイル受け取り
        if 'file' not in request.files:
            raise AppError("ファイルが選択されていません", http_status=400)
                
        file = request.files['file']
        filename = file.filename
        img_path = str(self.basedir / "data" / "input" / filename )
        file.save(img_path)

        # ファイルのロードに失敗した場合の処理
        if img_path is None:
            logger.error("ファイルが空です")
            raise AppError('ファイルが空です', http_status=400)

        # ファイル名チェック
        if filename == '' or filename is None:
            logger.error("ファイル名が空です")
            raise AppError('ファイル名がありません', http_status=400)
        
        #拡張子チェック
        ext = self.extension_split(img_path)
        logger.info("拡張子:" + ext)
        if ext.lower() not in [".jpeg", ".jpg", ".png", ".heic"]:
            logger.error('AIがファイル拡張子に対応していません')
            raise AppError("ファイルが拡張子に対応していません", http_status=400)

        #HEICのJPEG変換
        if ext == ".HEIC":
            img_path = self.heic_convert(img_path)
            logger.info("from heic to jpeg:" + img_path)

        #ファイル名の変更と上書き
        img_path = self.filename_convert(img_path)
        logger.info("file rename " + img_path)        

        return img_path, filename
    
    def preprocess_twoface(self, file):
        filename = file.filename
        img_path = str(self.basedir / "data" / "input" /filename)
        file.save(img_path)

        # ファイルのロードに失敗した場合の処理
        if img_path is None:
            logger.error("ファイルが空です")
            raise AppError('ファイルが空です', http_status=400)

        # ファイル名チェック
        if filename == '' or filename is None:
            logger.error("ファイル名が空です")
            raise AppError('ファイル名がありません', http_status=400)
        
        #拡張子チェック
        ext = self.extension_split(img_path)
        logger.info("拡張子:" + ext)
        if ext.lower() not in [".jpeg", ".jpg", ".png", ".heic"]:
            logger.error('AIがファイル拡張子に対応していません')
            raise AppError("ファイルが拡張子に対応していません", http_status=400)

        #HEICのJPEG変換
        if ext == ".HEIC":
            img_path = self.heic_convert(img_path)
            logger.info("from heic to jpeg:" + img_path)

        #ファイル名の変更と上書き
        img_path = self.filename_convert(img_path)
        logger.info("file rename " + img_path)        

        return img_path, filename







    
