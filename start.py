# -- coding: utf-8 --
import os
from glob import glob
from flask import Flask, jsonify, render_template, request, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
import requests

from random import randint
from yolo_detect import detect_img


PEOPLE_FOLDER = os.path.join('static', 'upload')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER



@app.route('/')  # 홈주소
def home():
    userfiles = glob(app.config['UPLOAD_FOLDER'] + '/origin/*')
    filenames = [os.path.split(file)[-1] for file in userfiles[:3]]
    return render_template('home.html', items=filenames)


@app.route('/about')  # 정보
def about():
    return render_template('about.html')


@app.route('/upload')  # 다른 사이트 양식 사용하기
def up_file():
    return render_template('upload.html')



@app.route('/fileUpload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        print(app.config['UPLOAD_FOLDER'], f)
        filename = str(randint(10000, 99999)) + '.jpg' # + '_' + filename
        origin_path = app.config['UPLOAD_FOLDER']+ '/origin/' + filename
        proc_path = app.config['UPLOAD_FOLDER']+ '/proc/' + filename
        f.save(origin_path)
        detect_img(origin_path, proc_path, car_dist_mode=False)
        # car_dist_mode 가 True => 차량 거리만 검출
        return redirect(url_for('uploaded_file', filename=filename))
    else:
        return redirect(url_for('up_file'))


@app.route('/show/<filename>')
def uploaded_file(filename):
    oimage = url_for('view_origin_file', filename=filename)
    pimage = url_for('view_proc_file', filename=filename)
    return render_template('imageshow.html', oimage=oimage, pimage=pimage)


@app.route('/uploads/origin/<filename>')
def view_origin_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER']+'/origin/', filename)

@app.route('/uploads/proc/<filename>')
def view_proc_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER']+'/proc/', filename)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port='8080')  # 외부 접속 가능
    app.run(host='127.0.0.1', port='8080', debug=True)  # 로컬 디버그모드
