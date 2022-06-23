
'''
install following package to do machine learning
pip install tensorflow
pip install keras
pip install numpy
pip install pillow
pip install scipy
'''


'''
This secton is Loading Model and Prediction

Load Model with “load_model”
Convert Images to Numpy Arrays for passing into ML Model
Print the predicted output from the model.
'''
from keras.models import load_model
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.utils import load_img

from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.applications.vgg16 import VGG16
import numpy as np

from keras.models import load_model

import os

# image name that is predicted
photo_name = 'photo_1127.jpg'


#load model to do predict with it
model = load_model('model_saved.h5')

#load image, format the image
image = load_img(photo_name, target_size=(640, 480))
img = np.array(image)
img = img / 255.0
img = img.reshape(1,640,480,3)

#predict this image
predict = (model.predict(img) > 0.5).astype("int32")
print(predict)

#  If the image is recorgnized as land,  Land increase 1
if predict[0][0] == 0:
    print('it is CLEAR')

# If the image is recorgnized as sea,  Sea increase 1            
if predict[0][0] == 1:
    print('it is CLOUDY')

if predict[0][0] == 2:
    print('it is OVERCAST')


