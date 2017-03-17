from flask import Flask
from flask import render_template, url_for
import os
from flask import request, redirect, send_from_directory
from werkzeug.utils import secure_filename
import json

#import preprocessing
#import Transcript

UPLOAD_FOLDER = 'music/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/home')
def goHome():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('AboutUs.html')

@app.route('/audio')
def audio():
    return render_template('Audio.html')

@app.route('/transcript', methods=['GET','POST'])
def transcript():
    #data = request.args.get('data','')
    #file_name = request.args.get('file','')
    ##preprocessing.PreProcess(file_name)
    ##parsed_data = Transcript.stringParse(data)
    ##output = Transcript.Project(parsed_data, file_name)
    output = "test"
    out = {}
    out['output'] = output
    json_out = json.dumps(out)
    print("More testing")
    return render_template('Transcript.html', out=json_out)
    #return "<h1>You're literally a piece of shit</h1>"
    #return render_template('index.html')

@app.route('/upload', methods=['GET','POST'])
def upload():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #return redirect(url_for('uploaded_file', filename=filename))
    return render_template('Audio.html')

@app.route('/music/<filename>')
def uploaded_file(filename):
    #return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    return render_template('Audio.html')
