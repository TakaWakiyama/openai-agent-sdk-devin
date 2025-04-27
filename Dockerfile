FROM python:3.11-slim

# Node.jsとgitのインストール
RUN apt-get update && apt-get install -y curl git \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g @openai/codex

# Python依存ライブラリインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコード配置
COPY . /app
WORKDIR /app

# Cloud Runはポート8080を使用
ENV PORT 8080
CMD ["python", "main.py"]