import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np

model = tf.keras.models.load_model('D:/Downloads/model.h5')

img = image.load_img('D:/Downloads/test/all/4.jpg', target_size=(150, 150))
img_array = image.img_to_array(img)
print(img_array.shape)
img_array=np.expand_dims(img_array, axis=0)
print(img_array.shape)
#classes = model.predict(imr_array)

"""test_datagen = ImageDataGenerator(rescale=1./255)

test_data = test_datagen.flow_from_directory('D:/Downloads/test/',
                                               target_size=(150,150),
                                               class_mode=None,
                                               batch_size=32)

Y_pred = model.predict(test_data, verbose=1).reshape(-1)

filenames=test_data.filenames

#Y_pred = [1 if pred > 0.5 else 0 for pred in Y_pred]

results=pd.DataFrame({"id":filenames,
                      "label":Y_pred})

"""