#API の概要

## 環境

python3.12
windows11

## アプリケーションルート

| パス                                  | 概要                        |
| ------------------------------------- | --------------------------- |
| http://localhost:5000/                | ヘルスチェック用            |
| http://localhost:5000/login           | 認証認可（JWT）             |
| http://localhost:5000/image/          | 顔写真不備判定（拡張中）    |
| http://localhost:5000/twoface         | 顔類似度判定(２枚画像 POST) |
| http://localhost:5000/face/register   | 顔特徴量 DB 登録            |
| http://localhost:5000/face/similarity | 顔特徴量比較                |

## /login リクエスト レスポンス

リクエスト
| body | 型 |
| -------- | --- |
| username | str |
| password | str |

レスポンス
| キー | 型 | 概要 |
| ------------ | --- | ------------------------------- |
| access_token | str | JWT トークンの値有効期限 1 時間 |

## /image POST リクエスト レスポンス

リクエスト
| body | 型 |
| ---- | -------------- |
| file | 画像(formData) |

レスポンス
| キー | 型 | 概要 |
| ---------- | --- | ----------------------- |
| mask | str | Mask or No Mask の値 |
| face_count | str | 検出した顔の数 |
| image | str | base64 エンコードデータ |

## /twoface POST リクエスト レスポンス

リクエスト
| body | 型 |
| ---- | ---- |
| file | 画像(formData) |
| file | 画像(formData) |

レスポンス
| キー | 型 | 概要 |
| ------- | --- | ------------------ |
| message | str | コサイン類似度の値 |

## /face/register POST リクエスト レスポンス

リクエスト
| キー | 型 |
| ---- | -------------- |
| file | 画像(formData) |
| user_id | user_id |

レスポンス
| キー | 型 | 値 |
| ------- | --- | ---------------------- |
| message | str | 顔特徴量を登録しました |

## /face/similarity POST リクエスト レスポンス

リクエスト
| キー | 型 |
| ---- | -------------- |
| file | 画像(formData) |
| user_id | user_id |

レスポンス
| キー | 型 | 概要 |
| ---------- | --- | ---- |
| id | str | id |
| user_id | str | id |
| similarity | str | id |

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

| filename                 | description                                                                     |
| ------------------------ | ------------------------------------------------------------------------------- |
| run.py                   | API 起動用ファイル                                                              |
| models\*                 | モデルファイルが格納される                                                      |
| api/config/\*            | DB などの設定ファイルが格納される                                               |
| api/models.py            | DB 情報の定義ファイル                                                           |
| api/**init**.py          | アプリケーションルート設定ファイル                                              |
| api/imperfect_predict.py | /image/の全体処理が記載されたファイル。前処理 ⇒ 推論 ⇒ 後処理の原則に基づき記載 |
| api/two_face_predict.py  | /face/の全体処理が記載されたファイル                                            |
| api/face_register.py     | /face/register の全体処理が記載されたファイル                                   |
| api/preparation.py       | 前処理用関数定義ファイル。各全体処理ファイル の前処理部分で参照される           |
| api/facemask/\*          | mask 検出に必要な推論スクリプトが格納される                                     |
| api/facerecognition/\*   | 顔認証に必要な推論スクリプトが格納される                                        |
| api/facedetection/\*     | 顔検出や複数顔検出に必要な推論スクリプトが格納される                            |
| api/postprocess.py       | 後処理用関数定義ファイル。各全体処理ファイル の後処理部分で参照される           |
| api/error.py             | エラーハンドリング用の関数定義ファイル。Except のエラー時に参照される           |

## Posgre のセットアップ

Windows に Posgre をインストールする場合は下記を参考  
https://qiita.com/tom-sato/items/037b8f8cb4b326710f71  
https://www.postgresql.org/download/windows/

pgvector の DB 反映  
https://qiita.com/sana_bungal/items/13366afb14ee1ebafff8

ライブラリのインストール

```
pip install psycopg2-binary SQLAlchemy pgvector
```

psycopg2-binary: PostgreSQL に接続するためのドライバ。  
SQLAlchemy: ORM（Object-Relational Mapping）ライブラリ。  
pgvector: SQLAlchemy で pgvector 拡張を使えるようにするライブラリ。

初期セットアップ

```
$env:FLASK_APP = "run.py"
$env:CONFIG = "local"
Remove-Item -Recurse -Force .\migrations
flask db init
flask db migrate -m "Initial migration"
```

SQLShell を使って、DB 接続し pgvector を入れる

```
CREATE EXTENSION vector;
```

migrations/versions/\*\_initial_migration.py に pg ベクターを入れる

```
import pgvector.sqlalchemy
```

最後にアップグレード

```
flask db upgrade
```

今後、モデルを変更する場合

```
$env:FLASK_APP = "run.py"
$env:CONFIG = "local"
flask db migrate -m "add new column"
flask db upgrade
```

upgrade で「NameError: name 'pgvector' is not defined」が出る場合

```
from pgvector.sqlalchemy import Vector

sa.Column('embedding', pgvector.sqlalchemy.vector.VECTOR(dim=512), nullable=True),部分を下記に変更
sa.Column('embedding', Vector(512), nullable=False),
```
