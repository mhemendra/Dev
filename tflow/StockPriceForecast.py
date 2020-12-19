import os
import csv
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def plot_series(time, series, format="-", start=0, end=None):
    plt.plot(time[start:end], series[start:end], format)
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.grid(True)

open_price = []
time_step=[]
index = 0
with open(r'D:/Downloads/NESTLEIND.csv') as file:
    csv_reader = csv.reader(file, delimiter=',')
    next(csv_reader)
    #sel_rows = [row for idx, row in enumerate(csv_reader) if idx>2]
    for row in csv_reader:
        index +=1
        time_step.append(index)
        open_price.append(float(row[4]))# If float not added then order missing in plots as its string

time_steps = np.array(time_step)

open_price = np.array(open_price)

"""min = np.min(open_price)
max = np.max(open_price)
open_price -= min
open_price /= max"""
#open = np.array(open_price)

#plt.figure(figsize=(10,6))
#plot_series(time_steps, open, start=6000)

def windowed_dataset(series, window_size, batch_size, shuffle_buffer_size):
    series = tf.expand_dims(series, axis=-1)
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size+1, shift=1,drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(window_size+1))
    ds = ds.shuffle(shuffle_buffer_size)
    ds = ds.map(lambda w: (w[:-1], w[-1]))
    return ds.batch(batch_size).prefetch(1)

def model_forecast(model, series, window_size):
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w:w.batch(window_size))
    ds = ds.batch(32).prefetch(1)
    forecast = model.predict(ds)
    return forecast

split_time = 2000
train_open = open_price[:split_time]
test_open = open_price[split_time:]

window_size = 10
batch_size = 16
shuffle_buffer_size = 1000

train_ds = windowed_dataset(train_open, window_size, batch_size, shuffle_buffer_size)

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv1D(filters=64, kernel_size=5, activation='relu', padding='causal',input_shape=[None, 1]),
    tf.keras.layers.LSTM(64, activation='relu', return_sequences=True),
    tf.keras.layers.LSTM(64, activation='relu'),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(metrics=['mae'], loss=tf.keras.losses.Huber(), optimizer='adam')
history = model.fit(train_ds, epochs=5)
model.save('stockOpen.h5')
#model.summary()

#model = tf.keras.models.load_model('stockOpen.h5')
#add +1 to loop if the last value is to be taken and predict the next totally new value

rnn_forecast = open_price[split_time-window_size:split_time]
for time in range((len(open_price) - split_time)):
    input = np.asarray(rnn_forecast[time:time + window_size]).reshape(-1,window_size,1)
    pred_out = model.predict(input)
    rnn_forecast = np.append(rnn_forecast, pred_out)
rnn_forecast = rnn_forecast[window_size:].reshape(-1,1)
forecast = np.array(rnn_forecast)[:, 0]

mae = tf.keras.metrics.mae(test_open,forecast).numpy()
print("mae::",mae)

#model.predict(np.expand_dims(open_price[split_time:split_time+window_size][np.newaxis], axis=-1))

"""rnn_forecast = []
for time in range(split_time-window_size, (len(open_price) - window_size)):
    input = open_price[time:time + window_size].reshape(-1,window_size,1)
    pred_out = model.predict(input)
    rnn_forecast.append(pred_out)
rnn_forecast = rnn_forecast[window_size:].reshape(-1,1)
forecast = np.array(rnn_forecast)[:,0,0]"""

"""plt.figure(figsize=(10, 6))
plot_series(time_steps[split_time:], test_open, 'r')
plot_series(time_steps[split_time:], forecast, 'y')"""