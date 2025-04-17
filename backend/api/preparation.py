from pathlib import Path
from flask import jsonify
import PIL
import os
from os.path import splitext
import pillow_heif
from PIL import Image
import uuid

basedir = Path(__file__).parent.parent

def load_image(request):
    try:
        """画像の読み込み"""
        # ファイルの受け取り
        if 'file' not in request.files:
            return None, None
        
        # 画像の受け取り
        file = request.files['file']
        
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

    
