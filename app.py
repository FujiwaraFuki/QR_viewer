from flask import Flask, render_template_string
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import os

# =========================
# 設定
# =========================

CSV_PATH1 = "sample_master.csv"
CSV_PATH2 = "location_master.csv"
CSV_PATH3 = "project_master.csv"
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

df1 = pd.read_csv(CSV_PATH1)
df2 = pd.read_csv(CSV_PATH2)
df3 = pd.read_csv(CSV_PATH3)

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
  <h2>サンプル概要</h2>
  <ul>
    {% for k, v in data1.items() %}
      <li><b>{{ k }}</b>: {{ v }}</li>
    {% endfor %}
  </ul>
  <h2>詳細</h2>
  <ul>
    {% for k, v in data2.items() %}
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

    # --- sample_master から該当行 ---
    row1 = df1[df1["sample_id"] == sample_id]
    if row1.empty:
        return "Sample ID not found", 404

    sample_data1 = row1.iloc[0, [0,2,3]].to_dict()
    sample_data2 = row1.iloc[0, 4:].to_dict()

    # --- location_id を取得 ---
    location_id = row1.iloc[0,].to_dict().get("location_id")

    # --- location_master から該当行 ---
    location_data1 = {}
    location_data2 = {}
    if location_id is not None:
        row2 = df2[df2["location_id"] == location_id]
        if not row2.empty:
            location_data1 = row2.iloc[0, [0,2,3]].to_dict()
            location_data2 = row2.iloc[0, 4:].to_dict()

    # --- project_id を取得 ---
    project_id = row2.iloc[0,].to_dict().get("project_id")

    # --- pproject_master から該当行 ---
    project_data1 = {}
    project_data2 = {}
    if project_id is not None:
        row3 = df3[df3["project_id"] == project_id]
        if not row3.empty:
            location_data3 = row3.iloc[0, 0:3].to_dict()
            location_data3 = row3.iloc[0, 3:].to_dict()

    # --- データを結合（同じ ul に出す） ---
    combined_data1 = {}
    combined_data1.update(project_data1)
    combined_data1.update(location_data1)
    combined_data1.update(sample_data1)

    combined_data2 = {}
    combined_data2.update(location_data2)
    combined_data2.update(sample_data2)
    combined_data2.update(project_data2)

    return render_template_string(HTML, data1=combined_data1, data2=combined_data2)

# =========================
# 起動
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
