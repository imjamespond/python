from flask import Flask, request, send_from_directory
import os

import chroma
import config

config.config_gpu()

app = Flask(__name__)
top_N = int(os.getenv("TOP_N", "10"))

UPLOAD_DIR = "uploads"
@app.route('/upload', methods=['POST'])
def upload():
    topN = int(request.form.get('topN', top_N))
    file = request.files.get('image')
    if not file:
        return {'error': '没有文件'}, 400
    
    # os.makedirs(UPLOAD_DIR, exist_ok=True)
    # path = os.path.join(UPLOAD_DIR, file.filename)
    # file.save(path)

    results = chroma.search_embeding(file, topN)

    print(results)

    return {'message': '上传成功', 'results': results}
# 直接 serve static/index.html
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)