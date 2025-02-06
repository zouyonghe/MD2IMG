from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mistune
import os
import uuid
import subprocess

app = Flask(__name__)
CORS(app)

SAVE_PATH = "static/images"
os.makedirs(SAVE_PATH, exist_ok=True)

@app.route("/static/images/<filename>")
def serve_image(filename):
    """ 允许访问生成的图片 """
    return send_from_directory(SAVE_PATH, filename)

def save_markdown_as_image(markdown_text):
    """ 渲染 Markdown 并用 Puppeteer 生成图片 """
    html_content = mistune.markdown(markdown_text)
    html_path = f"{SAVE_PATH}/{uuid.uuid4()}.html"
    image_path = f"{SAVE_PATH}/{uuid.uuid4()}.png"

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(f"<html><body>{html_content}</body></html>")

    try:
        subprocess.run(["node", "render.js", html_path, image_path], check=True)
    except subprocess.CalledProcessError as e:
        print("Puppeteer 渲染失败:", e)
        return None

    os.remove(html_path)  # 删除临时 HTML
    return image_path

@app.route("/render", methods=["POST"])
def render_markdown():
    data = request.json
    markdown_text = data.get("markdown", "")

    if not markdown_text:
        return jsonify({"error": "No Markdown provided"}), 400

    image_path = save_markdown_as_image(markdown_text)
    if not image_path:
        return jsonify({"error": "Image generation failed"}), 500

    image_url = request.host_url + "static/images/" + os.path.basename(image_path)
    return jsonify({"image_url": image_url})

if __name__ == "__main__":
    app.run(debug=True)
