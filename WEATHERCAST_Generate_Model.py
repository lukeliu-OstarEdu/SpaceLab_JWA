train_data_dir = 'data/train'
validation_data_dir = 'data/validation'
nb_train_samples = 52 + 41 + 22
nb_validation_samples = 52 + 41 + 22
epochs = 5
batch_size = 10
img_width, img_height = 640, 480
'''
This part is to check the data format i.e the RGB channel is coming first or last so,
whatever it may be, the model will check first and then input shape will be fed accordingly.
'''
if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

'''
Conv2D is the layer to convolve the image into multiple images 
Activation is the activation function. 
MaxPooling2D is used to max pool the value from the given size matrix and same is used for the next 2 layers. then, Flatten is used to flatten the dimensions of the image obtained after convolving it. 
Dense is used to make this a fully connected model and is the hidden layer. 
Dropout is used to avoid overfitting on the dataset. 
Dense is the output layer contains only one neuron which decide to which category image belongs.
'''

model = Sequential()
model.add(Conv2D(32, (2, 2), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (2, 2)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (2, 2)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))


'''
Compile function is used here that involve the use of loss, optimizers and metrics.
Here loss function used is binary_crossentropy, optimizer used is rmsprop.
'''

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

'''
Now, the part of dataGenerator comes into the figure. In which we have used: 

ImageDataGenerator that rescales the image, applies shear in some range,
zooms the image and does horizontal flipping with the image.
This ImageDataGenerator includes all possible orientation of the image.

train_datagen.flow_from_directory is the function that is used
to prepare data from the train_dataset directory,
Target_size specifies the target size of the image.

test_datagen.flow_from_directory is used to prepare test data for the model and
all is similar as above.

fit_generator is used to fit the data into the model made above,
other factors used are steps_per_epochs tells us about the number of times
the model will execute for the training data. 
epochs tells us the number of times model will be trained in forward and backward pass. 
validation_data is used to feed the validation/test data into the model. 
validation_steps denotes the number of validation/test samples.
'''
train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='binary')
validation_generator = test_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='binary')

model.fit_generator(
        train_generator,
        steps_per_epoch=nb_train_samples // batch_size,
        epochs=epochs,
        validation_data=validation_generator,
        validation_steps=nb_validation_samples // batch_size)

classes = train_generator.class_indices
print('classes are ', classes)

'''
At last, we can also save the model.
'''

model.save('model_saved.h5')