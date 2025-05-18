from flask_sqlalchemy import SQLAlchemy
from pgvector.sqlalchemy import Vector
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # werkzeug.security.generate_password_hash() でハッシュ化した文字列を格納
    password = db.Column(db.String(250), nullable=False)
    #created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class FaceEmbedding(db.Model):
    __tablename__ = 'face_embeddings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    embedding = db.Column(Vector(512))  # 512次元のベクトルなど