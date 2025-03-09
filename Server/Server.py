from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid

app = Flask(__name__)
CORS(app)

# 新增存储路径配置[8](@ref)
TEXT_FILE = 'test.txt'
IMAGE_FOLDER = 'images'

@app.route('/api/v1/chat', methods=['POST'])
def handle_chat():
    text = request.form.get('text', '')
    image = request.files.get('image')

    # 文本存储逻辑[1](@ref)
    if text:
        with open(TEXT_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{text}\n")  # 追加写入并换行

    # 图片存储逻辑[3,7](@ref)
    filename = None
    if image and allowed_file(image.filename):
        ext = image.filename.split('.')[-1].lower()
        filename = f"{uuid.uuid4()}.{ext}"
        image.save(os.path.join(IMAGE_FOLDER, filename))  # 修改存储路径

    return jsonify({
        "reply": "已收到您的消息",
        "text_received": text,
        "image_path": f"/{IMAGE_FOLDER}/{filename}" if filename else None
    })

# 新增图片访问路由[8](@ref)
@app.route(f'/{IMAGE_FOLDER}/<filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

if __name__ == '__main__':
    # 创建多级目录[5](@ref)
    os.makedirs(IMAGE_FOLDER, exist_ok=True)
    if not os.path.exists(TEXT_FILE):
        open(TEXT_FILE, 'w').close()  # 创建空文本文件
    app.run(port=5000, debug=True)