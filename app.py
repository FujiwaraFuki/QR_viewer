from flask import Flask, render_template_string
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import os

# =========================
# 設定
# =========================

CSV_PATH = "sample_master.csv"
HOST = "0.0.0.0"
PORT = 8000

# Basic認証ユーザー（適宜変更）
users = {
    "symbio": generate_password_hash("ichihashi9118")
}

# =========================
# 初期化
# =========================

app = Flask(__name__)
auth = HTTPBasicAuth()

df = pd.read_csv(CSV_PATH)

# =========================
# 認証処理
# =========================

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users[username], password):
        return username

# =========================
# HTML（スマホ向け）
# =========================

HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Analysis Info</title>
  <style>
    body { font-family: sans-serif; padding: 10px; }
    h2 { border-bottom: 2px solid #444; }
    li { margin: 6px 0; }
  </style>
</head>
<body>
  <h2>解析サンプル情報</h2>
  <ul>
    {% for k, v in data.items() %}
      <li><b>{{ k }}</b>: {{ v }}</li>
    {% endfor %}
  </ul>
</body>
</html>
"""

# =========================
# ルーティング
# =========================

@app.route("/sample/<sample_id>")
@auth.login_required
def show_sample(sample_id):
    row = df[df["sample_id"] == sample_id]

    if row.empty:
        return "Analysis ID not found", 404

    data = row.iloc[0].to_dict()
    return render_template_string(HTML, data=data)

# =========================
# 起動
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
