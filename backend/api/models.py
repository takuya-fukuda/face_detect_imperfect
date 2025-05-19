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

    # FaceEmbedding との一対一のリレーション
    embedding = db.relationship(
        'FaceEmbedding',
        back_populates='user',
        uselist=False,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<User {self.username}>'

class FaceEmbedding(db.Model):
    __tablename__ = 'face_embeddings'

    # username を主キーかつ外部キーとして設定
    username = db.Column(
        db.String(80),
        db.ForeignKey('users.username', ondelete='CASCADE'),
        primary_key=True
    )
    embedding = db.Column(Vector(512))  # 512次元のベクトルなど

    # User 側とのリレーション
    user = db.relationship('User', back_populates='embedding')

    def __repr__(self):
        return f'<FaceEmbedding username={self.username}>'
