import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import cv2
import os

#def detect_faces(img_path: str, model_path: str = "detector.tflite") -> str:
def detect_faces(img_path: str, model_path: str = "./model/detector.tflite") -> str:
    """
    顔検出を行い、検出された顔にバウンディングボックスを描画して保存する関数

    Parameters:
        img_path (str): 入力画像のパス
        model_path (str): tfliteモデルファイルのパス（デフォルト: 'detector.tflite'）

    Returns:
        str: 保存された画像のパス
    """

    # モデルロード
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.FaceDetectorOptions(base_options=base_options)
    detector = vision.FaceDetector.create_from_options(options)

    # 画像ロード
    mp_image = mp.Image.create_from_file(img_path)
    input_image = cv2.imread(img_path)

    # 顔検出
    face_detector_result = detector.detect(mp_image)

    if not face_detector_result.detections:
        print("顔が検出されませんでした！")
    else:
        num_faces = len(face_detector_result.detections)
        if num_faces == 1:
            print("1つの顔が検出されました！")
        else:
            print(f"複数の顔が検出されました！（{num_faces}個）")

        # バウンディングボックス描画
        for detection in face_detector_result.detections:
            bbox = detection.bounding_box
            start_point = (bbox.origin_x, bbox.origin_y)
            end_point = (bbox.origin_x + bbox.width, bbox.origin_y + bbox.height)
            cv2.rectangle(input_image, start_point, end_point, (255, 0, 0), 2)

    # 保存
    base_filename = os.path.splitext(os.path.basename(img_path))[0]
    output_path = f"./data/result/{base_filename}_boxes.jpg"
    #output_path = f"./{base_filename}_boxes.jpg"
    cv2.imwrite(output_path, input_image)
    print(f"保存しました: {output_path}")

    return { "face_count": num_faces, "output_path": output_path }

#output_file = detect_faces("face1.jpg")
