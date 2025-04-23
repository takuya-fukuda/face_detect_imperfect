from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import cv2
import os


def mask_judge(img_path, filename):
    # モデルの読み込み
    model = load_model('./model/mymodel.h5')

    # パス設定
    #img_path = './img/1-with-mask.jpg'  # 推論したい画像
    #output_path = './result/with_bbox.jpg'
    print(img_path)
    output_path = './data/result/' + filename
    os.makedirs('./data/result/', exist_ok=True)
    print(output_path)

    img = image.load_img(img_path, target_size=(150, 150, 3))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    # 推論
    res=model.predict(img_array)
    prediction = model.predict(img_array)[0][0]

    if prediction > 0.5:
        print("😷 → マスクなし (NO MASK)")
        return {"mask": "No Mask", "result_path": img_path}
    else:
        print("🟢 → マスクあり (MASK)")
        return {"mask": "Mask", "result_path": img_path}
    

    # # OpenCVで画像読み込み（顔検出のため）
    # original_img = cv2.imread(img_path)
    # gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)

    # # 顔検出用カスケード
    # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # for (x, y, w, h) in faces:
    #     # 顔領域を切り出してリサイズ
    #     face = original_img[y:y+h, x:x+w]
    #     #resized_face = cv2.resize(face, (150, 150))
    #     img_array = image.img_to_array(img_path, target_size=(150, 150, 3))
    #     img_array = np.expand_dims(img_array, axis=0)

    #     # 推論
    #     prediction = model.predict(img_array)[0][0]

    #     print(prediction)

    #     # ラベルと色の設定
    #     if prediction > 0.5:
    #         label = "No Mask"
    #         color = (0, 0, 255)  # 赤
    #     else:
    #         label = "Mask"
    #         color = (0, 255, 0)  # 緑

        # BBOXとラベルを描画
    #     cv2.rectangle(original_img, (x, y), (x+w, y+h), color, 2)
    #     cv2.putText(original_img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # # 結果画像を保存
    # cv2.imwrite(output_path, original_img)
    # print(f"BBOX付き画像を保存しました: {output_path}")

    # return {"mask": label, "result_path": output_path}
