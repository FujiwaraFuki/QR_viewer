import qrcode
import sys

if len(sys.argv) != 2:
    print("Usage: python make_qr.py <SAMPLE_ID>")
    sys.exit(1)

sample_id = sys.argv[1]

url = f"https://qr-viewer-25ny.onrender.com//sample/{sample_id}"

img = qrcode.make(url)
img.save(f"qr_codes/{sample_id}.png")

print(f"Saved QR: {sample_id}.png")
