import numpy as np
import pandas as pd
import tensorflow as tf

names = pd.read_csv(r'C:\Users\mheme\Desktop\Dinos.csv').values
names = [item.lower() for sublist in names for item in sublist]
total_names = len(names)
name_chars=[]
chars = set()
for i in range(total_names):
    single_name = names[i]
    single_name_chars = [c for c in single_name]
    name_chars.append(single_name_chars)
    chars = chars.union(single_name_chars)
chars = sorted(chars.union(['BOF','EOF']))
total_chars = len(chars)
char_to_ix = {ch:i for i,ch in enumerate(chars)}
ix_to_char = {i:ch for i,ch in enumerate(chars)}

train_x, train_y = [],[]
for name in name_chars:
    name = [char_to_ix[char] for char in name]
    train_x.append([char_to_ix['BOF']]+name)
    train_y.append(name+[char_to_ix['EOF']])

"""max_lengths = 14
train_x = [x for x in train_x if len(x)==14]
train_y = [x for x in train_y if len(x)==14]"""

"""for name in train_y:
    name = [ix_to_char[char] for char in name]
    print(name)"""

#train_x = np.array(train_x).reshape(-1,14,1).astype(np.float32)
#train_y = np.array(train_y).reshape(-1,14,1).astype(np.float32)
max_length = max([len(x) for x in train_x])
padded_x = tf.keras.preprocessing.sequence.pad_sequences(train_x).reshape(-1,max_length,1).astype(np.float32)
padded_y = tf.keras.preprocessing.sequence.pad_sequences(train_y).reshape(-1,max_length,1)

"""padded_x = np.array(padded_x)
padded_y = np.array(padded_y)"""

model = tf.keras.models.Sequential([
    #Embedding(total_chars, 128, input_length=14),
    tf.keras.layers.Masking(mask_value=0),
    tf.keras.layers.SimpleRNN(16, return_sequences=True,activation='relu'),
    tf.keras.layers.Dense(total_chars,activation='softmax')
])
model.compile(optimizer='adam', metrics=['accuracy'], loss='sparse_categorical_crossentropy')
model.fit(padded_x,padded_y,epochs=200)
model.save('dino.h5')
