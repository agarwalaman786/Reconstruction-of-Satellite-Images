#Importig Libraries
from flask import *  
from werkzeug.utils import secure_filename

from skimage.io import imread, imsave
from inpainter import Inpainter
#Removung the using tesnorflow backend
import os
import sys
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
from keras.models import model_from_json
from keras.models import load_model
from keras.preprocessing.image import array_to_img, img_to_array, load_img, ImageDataGenerator
from keras import backend as K
import imageio

sys.stderr = stderr
import numpy as np
import PIL
from PIL import Image
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

import tensorflow as tf
import cv2
import boto3
import json
import gc
#To remove the warnings
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'


with open('config.json') as config_file:
    data = json.load(config_file)

s3 = boto3.resource('s3', endpoint_url=data['endpoint_url'],aws_access_key_id=data['aws_access_key_id'],
    aws_secret_access_key=data['aws_secret_access_key'])


#If tensorflow with gpu is being used
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)

#Loading the JSON file here
json_file = open('model_num.json', 'r')

#Loading the models
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

#load weights into new model
loaded_model.load_weights("model_num.h5")
#print("Loaded model from disk")
dims = [256, 256]
graph = tf.get_default_graph()

app = Flask(__name__)

#Uploading files where the files would be store which the user uploaded
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploaded_files/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloaded_files/'
my_bucket = s3.Bucket(data['bucketName'])

#app configuration or global variables
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER


#Allowed Extensions of files being uploaded
ALLOWED_EXTENSIONS = {'jpg','JPEG','PNG','png','TIF','tif','jpeg'}
def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#Image Inpainting Method
def Image_Inpainting(Org_Image,Target_Image,filename,org_dims):
    image = imread(Org_Image)
    mask = imread(Target_Image, as_grey=True)

    output_image = Inpainter(
        image,
        mask,
        filename,
        patch_size=9,
        plot_progress=True,
    ).inpaint()
    imsave(os.path.join(app.config['DOWNLOAD_FOLDER'],filename), output_image, quality=100)
    path = os.path.dirname(os.path.abspath(__file__)) + '/Gif/'+filename.split('.')[0] + '.gif'
    folder_Name = 'downloaded_files/'
    my_bucket.upload_file(os.path.join(app.config['DOWNLOAD_FOLDER'],filename),folder_Name+filename)

    folder_Name = 'GIF/'
    print(path)
    my_bucket.upload_file(path, folder_Name+filename.split('.')[0]+'.gif')

    

#Applying the Model Here
def process_file(path,filename):
    global graph
    with graph.as_default():
        image_name = path + filename
        img = Image.open(image_name).convert('RGB')
        org_dims = img.size
        resized_img = img.resize((dims),Image.ANTIALIAS)
        array_img = img_to_array(resized_img)/255
        array_img = np.array(array_img)
        predicted_mask = loaded_model.predict(array_img[np.newaxis, :, :, :])
        predicted_mask = predicted_mask.reshape(256, 256)
        threelevelmask = np.copy(predicted_mask)
        threshold1 = 0.3
        threshold2 = 0.6
        [rows, cols] = threelevelmask.shape
        newmask = np.zeros([rows, cols])
        for i in range(rows):
            for j in range(cols):
                if threelevelmask[i,j]<threshold1:
                    newmask[i,j] = 0
                if (threshold1<threelevelmask[i,j]) and (threelevelmask[i,j]<threshold2):
                    newmask[i,j] = 126
                if (threelevelmask[i,j]>threshold2):
                    newmask[i,j] = 255
        newmask = np.dstack([newmask, newmask, newmask])

        #Saving the mainfile here
        matplotlib.image.imsave(image_name,array_img)
        folder_Name = 'uploaded_files/'
        my_bucket.upload_file(image_name,folder_Name+filename)


        cmap = plt.cm.coolwarm
        norm = plt.Normalize(vmin=predicted_mask.min(), vmax=predicted_mask.max())
        new_image = cmap(norm(predicted_mask))        

        
        #Saving the Predicted mask here
        loc_file = os.path.join(app.config['UPLOAD_FOLDER'],'mask_'+filename)
        matplotlib.image.imsave(loc_file,np.uint8(newmask))
        my_bucket.upload_file(loc_file,folder_Name+'mask_'+filename)


        #Applying Image inpainting Method by this function
        Image_Inpainting(image_name,loc_file,filename,org_dims)




#Method to create .gif for the current images
@app.route('/Instructions')
def Instructions():
    return render_template('Instruction.html')


@app.route('/Gif/<filename>')
def make_gif(filename):
    path = os.path.dirname(os.path.abspath(__file__)) + '/Gif/'+filename.split('.')[0]+'.gif'
    fname = 'GIF/'+filename.split('.')[0]+'.gif'
    obj = list(my_bucket.objects.filter(Prefix=fname))
    if os.path.isfile(path):
        return send_file(path,as_attachment = False)
    if len(obj)>0:
        output = filename.split('.')[0]+'.gif'
        my_bucket.download_file(fname,output)
        return send_file(output,as_attachment=False)
    abort(404,'file not found')



@app.route('/downloaded_file/<filename>')
def download_file(filename):
    try:
        filename = filename.split('.')[0]
        output = filename+'.jpg'
        my_bucket.download_file('downloaded_files/'+filename+'.jpg',output)
        return send_file(output,as_attachment=True)
    except:
        abort(404,'file not found')


@app.route('/')  
def upload():  
    return render_template('main_page.html')  

     
@app.route('/success', methods = ['POST'])  
def success():  
    #Receiving the file from the front end
    if request.method == 'POST': 
        if 'file' not in request.files:
            #print('No file attached in request')
            return redirect(request.url)

        f = request.files['file']
        if f.filename=='':
            #having some error in png files
            #print('No file selected')
            return redirect(request.url)
        if f and allowed_file(f.filename):
            fname = secure_filename(f.filename)
            dirname = fname.split('.')[0]
            filename = 'downloaded_files/'+dirname+'.jpg'
            obj = list(my_bucket.objects.filter(Prefix=filename))
            path = os.path.join(os.path.dirname(os.path.abspath(__file__))) + '/Patches/' + dirname+'/'
            if len(obj)>0 or os.path.isdir(path):
                return "<h1>File With this Name Already Exists</h1><p>Please, Rename your file</p>"

            lst = fname.split('.')
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], fname));
            img.convert('RGB').save(os.path.join(app.config['UPLOAD_FOLDER'], lst[0]+'.jpg'))
            fname = lst[0]+'.jpg'
            process_file(app.config['UPLOAD_FOLDER'], fname)
            return redirect(url_for('download_file', filename=fname))
    return render_template('main_page.html')  


if __name__ == '__main__':  
    app.run(host='0.0.0.0',port=8080, debug=True)  