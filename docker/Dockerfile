FROM python:3.12

# gitは不要になったので削除（vimやlibgl1は必要なら残す）
RUN apt-get update && \
    apt-get install -y vim libgl1 && \
    rm -rf /var/lib/apt/lists/*

# 作業ディレクトリ作成
WORKDIR /api

# アプリ本体をコピー（コンテキスト=NII_API 基準）
COPY backend /api/backend

# 作業ディレクトリを移動（run.py があるディレクトリ）
WORKDIR /api/backend

RUN pip install --no-cache-dir -r requirements.txt

# ログディレクトリ作成 & 権限付与
RUN mkdir -p /api/logs && \
    chmod -R 755 /api/logs

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]