#API の概要

## 環境

python3.12
windows11

## アプリケーションルート

| パス                         | 概要             |
| ---------------------------- | ---------------- |
| http://localhost:5000/       | ヘルスチェック用 |
| http://localhost:5000/image/ | 顔写真マスク判定 |
| http://localhost:5000/face/  | 顔類似度判定     |

## /image POST リクエスト

| body               | 型  |
| ------------------ | --- |
| 画像データ(base64) | ?   |

## /image レスポンス

| キー  | 型  | 概要                    |
| ----- | --- | ----------------------- |
| mask  | str | Mask or No Mask の値    |
| image | str | base64 エンコードデータ |

## /face POST リクエスト

| body               | 型  |
| ------------------ | --- |
| 画像データ(base64) | ?   |
| 画像データ(base64) | ?   |

## /face POST レスポンス

| キー    | 型  | 概要               |
| ------- | --- | ------------------ |
| message | str | コサイン類似度の値 |

## 起動方法

1.Window 上に WSL 経由で Ubuntu アプリをインストール
以下 Ubuntu アプリ内で実行

3.git のインストール
sudo apt-get install git

4.仮想環境の作成
python3.10 -m venv [your_env_name]

cd [your_env_name]

source bin/activate

## 本番セットアップ

1. env 環境内に Gunicorn のインストール
   pip install gunicorn
   gunicorn --version

2. Flask のデバックを False
   run.py を参照し「app.run(host='0.0.0.0', port=5000, debug=True)」となっている場合は False に変更

3. Gunicorn で起動
   gunicorn -w 4 -b 0.0.0.0:5000 run:app --access-logfile access.log --error-logfile error.log --log-level debug

ワーカ数：4
バインドするアドレスとポート：0.0.0.0:8000
Python ファイル名と Flask アプリケーション名：run:app
アクセスログ：access.log
エラーログ：error.log
ログレベル：debug

## Flask フォルダ構成

| filename               | description                                                                     |
| ---------------------- | ------------------------------------------------------------------------------- |
| run.py                 | API 起動用ファイル                                                              |
| models\*               | モデルファイルが格納される                                                      |
| api/config/\*          | DB などの設定ファイルが格納される                                               |
| api/models.py          | DB 情報の定義ファイル                                                           |
| api/**init**.py        | アプリケーションルート設定ファイル                                              |
| api/mask_predict.py    | /image/の全体処理が記載されたファイル。前処理 ⇒ 推論 ⇒ 後処理の原則に基づき記載 |
| api/face_predict.py    | /face/の全体処理が記載されたファイル                                            |
| api/preparation.py     | 前処理用関数定義ファイル。mask_predict の前処理部分で参照される                 |
| api/facemask/\*        | mask 検出に必要な推論スクリプトが格納される                                     |
| api/facerecognition/\* | 顔認証に必要な推論スクリプトが格納される                                        |
| api/postprocess.py     | 後処理用関数定義ファイル。mask_predict から後処理部分で参照される               |
| api/error.py           | エラーハンドリング用の関数定義ファイル。Except のエラー時に参照される           |
