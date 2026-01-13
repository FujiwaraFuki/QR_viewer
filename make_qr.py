import qrcode
from PIL import Image, ImageDraw, ImageFont
import sys
import os

# =========================
# 設定（ここが重要）
# =========================

BASE_URL = "https://qr-viewer-25ny.onrender.com/sample"
OUT_DIR = "qr_codes"

QR_SIZE = 160          # ← QRを大きく（400 → 600）
TEXT_HEIGHT = 10      # ← 文字エリア拡大
FONT_SIZE = 200        # ← 文字を大きく

BG_COLOR = "white"
QR_COLOR = "black"

os.makedirs(OUT_DIR, exist_ok=True)

# =========================
# 引数
# =========================

if len(sys.argv) != 2:
    print("Usage: python make_qr.py <SAMPLE_ID>")
    sys.exit(1)

sample_id = sys.argv[1]
url = f"{BASE_URL}/{sample_id}"

# =========================
# QRコード生成
# =========================

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_Q,
    box_size=12,   # ← モジュールサイズも大きく
    border=4,
)

qr.add_data(url)
qr.make(fit=True)

qr_img = qr.make_image(
    fill_color=QR_COLOR,
    back_color=BG_COLOR
).convert("RGB")

qr_img = qr_img.resize((QR_SIZE, QR_SIZE), Image.NEAREST)

# =========================
# キャンバス作成
# =========================

canvas = Image.new(
    "RGB",
    (QR_SIZE, QR_SIZE + TEXT_HEIGHT),
    BG_COLOR
)

canvas.paste(qr_img, (0, 0))

draw = ImageDraw.Draw(canvas)

# フォント
try:
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", FONT_SIZE)
except IOError:
    font = ImageFont.load_default()

# 中央揃え
bbox = draw.textbbox((0, 0), sample_id, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

text_x = (QR_SIZE - text_width) // 2
text_y = QR_SIZE + (TEXT_HEIGHT - text_height) // 2

draw.text(
    (text_x, text_y),
    sample_id,
    fill="black",
    font=font
)

# =========================
# 保存
# =========================

out_path = os.path.join(OUT_DIR, f"{sample_id}.png")
canvas.save(out_path)

print(f"Saved high-res QR image: {out_path}")
