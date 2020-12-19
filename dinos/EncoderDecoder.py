import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

names= pd.read_csv(r'C:\Users\mheme\Desktop\GOT Names.csv', header=None).values
names = [item.lower() for sublist in names for item in sublist]
total_names = len(names)
name_chars = []
chars = set()
for i in range(len(names)):
    single_name = names[i]
    single_name_chars = [c for c in single_name]
    chars = chars.union(set(single_name_chars))
    name_chars.append(single_name_chars)
total_chars = len(chars) + 3 #1 each for 66,99 and pad(0)
char_to_ix = { ch:i+1 for i,ch in enumerate(chars) }
ix_to_char = { i+1:ch for i,ch in enumerate(chars) }

#name_chars = [sinlge_name_list for sinlge_name_list in name_chars for chars in sinlge_name_list]

name_X,name_Y = [],[]
for i in range(len(name_chars)):
    name_chars[i] = [char_to_ix[chars] for chars in name_chars[i]]
    name_X.append([28] + name_chars[i])
    name_Y.append(name_chars[i] + [29])

print(name_X)

max_length = max([len(x) for x in name_X])
padded_X = pad_sequences(name_X, maxlen=max_length, padding='post')
padded_Y = pad_sequences(name_Y, maxlen=max_length, padding='post')

padded_X = np.array(padded_X).reshape(total_names, max_length, 1)
padded_Y = np.array(padded_Y).reshape(total_names, max_length, 1)

"""padded_X = tf.cast(padded_X, tf.float32)
padded_Y = tf.cast(padded_Y, tf.float32)"""

model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(100, return_sequences=False, activation='relu', input_shape=(22, 1)),
    tf.keras.layers.RepeatVector(22),
    tf.keras.layers.LSTM(100, activation='relu', return_sequences=True),
    tf.keras.layers.Dense(1)])

model.compile(loss='mse', metrics=['accuracy'], optimizer='adam')
model.fit(padded_X, padded_Y, epochs=100)