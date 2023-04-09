# ベースイメージとしてPython3.9のAlpineイメージを使用
FROM python:3.9-alpine

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
RUN apk add --no-cache gcc musl-dev postgresql-dev

## 仮想環境を作成
#RUN python -m venv /app/venv

## 仮想環境をアクティベート
#ENV PATH="/app/venv/bin:$PATH"

# requirements.txtをコピー
COPY requirements.txt .

# Pythonライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . .

# ポート番号を設定
EXPOSE 5555

# アプリケーションを実行
CMD ["gunicorn", "--workers", "4", "--threads", "48", "--worker-class", "gthread", "-b", "0.0.0.0:5555", "flaskr:create_app()"]
