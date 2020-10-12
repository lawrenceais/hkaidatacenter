
import os
#from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
from PIL import Image
import sys
import time


endpoint = "https://hkaidatacenter.cognitiveservices.azure.com/"
subscription_key = "19d0daa4621a40988050683d074e8a2a"
remote_image_folder = "http://52.237.112.242/static/uploads/"

def brandDetection(filename):
    result = []
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    remote_image_features = ["brands"]
    remote_image_url = remote_image_folder + filename
    detect_brands_results_remote = computervision_client.analyze_image(remote_image_url, remote_image_features)
    if len(detect_brands_results_remote.brands) == 0:
        #print("No brands detected.")
        record = ("name", "Not Found")
        result.append(record)
    else:
        for brand in detect_brands_results_remote.brands:
            record = ("name", brand.name)
            result.append(record)
            record = ("confidence","{:.1f}%".format(brand.confidence * 100))
            result.append(record)
            r_x1 = ("x1", brand.rectangle.x)
            r_x2 = ("x2", brand.rectangle.x + brand.rectangle.w)
            r_y1 = ("y1", brand.rectangle.y)
            r_y2 = ("y2", brand.rectangle.y + brand.rectangle.h)
            record = ("rectangle",r_x1, r_x2, r_y1, r_y2)
            result.append(record)
            '''
            result = result + "'{}' brand detected with confidence {:.1f}% at location {}, {}, {}, {}".format( \
                brand.name, brand.confidence * 100, brand.rectangle.x, brand.rectangle.x + brand.rectangle.w, \
                brand.rectangle.y, brand.rectangle.y + brand.rectangle.h) 
            '''
    return result


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash("No File")
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
        
        # Call function for brand detection
        bd_result = brandDetection(filename)
        for x in range(len(bd_result)): 
            flash(bd_result[x])
        
		#flash('Image successfully uploaded and displayed')
        return render_template('recognition.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)
    
@app.route('/upload')
def upload():
    return render_template("upload.html")

@app.route('/result')
def result():
    return render_template("result.html")


@app.route('/display/<filename>')
def display_image(filename):
	print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=80)
