from flask import Flask, request, render_template, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']  # 获取上传的文件

        # 保存文件
        file.save('uploads/' + secure_filename(file.filename))

        return '上传成功！'
    return render_template('upload.html')


@app.route('/display')
def display():
    filename = 'uploads/example.jpg'  # 图片路径

    return render_template('display.html', filename=filename)
