import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
import tensorflow as tf


char_to_ix = {'\n': 0, '#': 1, 'a': 2, 'b': 3, 'c': 4, 'd': 5, 'e': 6, 'f': 7, 'g': 8, 'h': 9, 'i': 10, 'j': 11, 'k': 12, 'l': 13, 'm': 14, 'n': 15, 'o': 16, 'p': 17, 'q': 18, 'r': 19, 's': 20, 't': 21, 'u': 22, 'v': 23, 'w': 24, 'x': 25, 'y': 26, 'z': 27}
ix_to_char = {0: '\n', 1: '#', 2: 'a', 3: 'b', 4: 'c', 5: 'd', 6: 'e', 7: 'f', 8: 'g', 9: 'h', 10: 'i', 11: 'j', 12: 'k', 13: 'l', 14: 'm', 15: 'n', 16: 'o', 17: 'p', 18: 'q', 19: 'r', 20: 's', 21: 't', 22: 'u', 23: 'v', 24: 'w', 25: 'x', 26: 'y', 27: 'z'}

def predict_names(model,sequence_length=5,start_string=""):
    endOfFile = 0
    input_string = start_string[-sequence_length:]
    pad_length = sequence_length - len(input_string)
    if(pad_length>0):
        input_string = '#'*pad_length + input_string
    input_model = [char_to_ix[c] for c in input_string]
    output = []
    predicted_out = 1
    while predicted_out!=endOfFile:
        predicted_out = model.predict(np.array(input_model).reshape(-1,sequence_length,1))
        predicted_out = np.random.choice(28, p=predicted_out.ravel())
        input_model = input_model[1:5] + [predicted_out]
        if(predicted_out!=endOfFile):
            output.append(predicted_out)
    output = [ix_to_char[c] for c in output]
    return start_string + "".join(output)

model = tf.keras.models.load_model("dino.h5")
for i in range(5):
    name_start = "dino"
    output = predict_names(model, 5, name_start.lower())
    print(output)

