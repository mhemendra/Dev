import tensorflow as tf
keras=tf.keras
KL=keras.layers
import numpy as np
from tensorflow.keras import layers
from tensorflow.keras import Model

local_weights_file = "D:/Downloads/inception_v3_weights_tf_dim_ordering_tf_kernels_notop.h5"
pre_trained_model = tf.keras.applications.inception_v3.InceptionV3(input_shape=(150,150,3),
                               include_top=False,
                               weights=local_weights_file)

for layer in pre_trained_model.layers:
    layer.trainable = False

last_layer = pre_trained_model.get_layer('mixed7')
last_output = last_layer.output

x = layers.Flatten()(last_output)
x = layers.Dense(128, activation='relu')(x)
x = layers.Dense(1, activation='sigmoid')(x)

model = Model(pre_trained_model.input, x)

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

train_datagen = tf.keras.preprocessing.ImageDataGenerator(
    rescale=1./255,
    zoom_range=0.2,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    fill_mode='nearest',
    horizontal_flip=True
    )

validation_datagen = tf.keras.preprocessing.ImageDataGenerator(rescale=1./255)

train_data = train_datagen.flow_from_directory('D:/Downloads/training/',
                                               target_size=(150,150),
                                               class_mode='binary',
                                               batch_size=32)

validation_data = validation_datagen.flow_from_directory('D:/Downloads/validation/',
                                               target_size=(150,150),
                                               class_mode='binary',
                                               batch_size=32)

keys = train_data.class_indices.keys()
print(train_data.labels[:10])
print(train_data.filenames[:10])
print(keys)
model.fit_generator(train_data, epochs=1, validation_data=validation_data)
model.save('D:/Downloads/model.h5')