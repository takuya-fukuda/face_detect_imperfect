import json
import os
from pathlib import Path

from flask import Flask
from flask_migrate import Migrate

from api.config import config 

from api import api
from api.models import db

from flask_cors import CORS

from api.config.logging_config import setup_logging #ログ設定追加

from flask_jwt_extended import JWTManager


jwt = JWTManager()

def create_app():
    setup_logging()  # ロギング設定を適用
    config_name = os.environ.get("CONFIG", "local")  # 環境変数から設定を取得、なければ "local"
    app = Flask(__name__)
    app.config.from_object(config[config_name])  # 該当する設定を適用

    db.init_app(app) # DBの初期化
    jwt.init_app(app) # JWTの初期化
    return app

app = create_app()
# DBマイグレーションの作成
Migrate(app, db)

#CORS
CORS(app)

# blueprintをアプリケーションに登録
app.register_blueprint(api)

#追加
if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, ssl_context=context, debug=False)
    app.run(host='0.0.0.0', port=5000, debug=False)
