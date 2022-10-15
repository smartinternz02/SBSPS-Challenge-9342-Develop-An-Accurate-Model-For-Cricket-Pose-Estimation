#app.py
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import numpy as np
from io import BytesIO
from tensorflow import keras
from tensorflow.keras.preprocessing import image

app = Flask(__name__)
index=['bowling','catch','cover drive','dive','flick','pull shot','scoop shot','square shot','straight drive','sweep']
UPLOAD_FOLDER = 'static/uploads/'
model=keras.models.load_model("C:/Users/USER/Desktop/Cricket/cricket.hdf5")
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)

        x=image.img_to_array(image.load_img("C:/Users/USER/Desktop/Cricket/WebApp/static/uploads/"+file.filename,target_size=(64,64)))
        x=np.expand_dims(x,axis=0)
        pred=np.argmax(model.predict(x),axis=1)
        flash(index[pred[0]])
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
 
if __name__ == "__main__":
    app.run(debug=True)