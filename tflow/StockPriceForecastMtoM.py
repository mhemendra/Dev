import csv
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Bidirectional, LSTM, Dense, Conv1D
import matplotlib.pyplot as plt

open_price = []
close_price =[]
time_step=[]
index = 0
with open('D:/Downloads/Individual_stocks/NESTLEIND.csv') as f:
    csvreader= csv.reader(f,delimiter=',')
    next(csvreader)
    for row in csvreader:
        open_price.append(float(row[1]))
        index = index + 1
        time_step.append(index)

open = np.array(open_price)
time_steps = np.array(time_step)

#plt.figure(figsize=(10,6))
#plt.plot(time_steps, open)

def windowed_dataset(series, window_size, batch_size, shuffle_buffer_size):
    series = tf.expand_dims(series, axis=-1)
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size+1, shift=1,drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(window_size+1))
    ds = ds.shuffle(shuffle_buffer_size)
    ds = ds.map(lambda w: (w[:-1], w[1:]))
    return ds.batch(batch_size).prefetch(1)

def model_forecast(model, series, window_size):
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w:w.batch(window_size))
    ds = ds.batch(32).prefetch(1)
    forecast = model.predict(ds)
    return forecast

def plot_series(time, series, format="-", start=0, end=None):
    plt.plot(time[start:end], series[start:end], format)
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.grid(True)

split_time = 1000
train_open = open[:split_time]
test_open = open[split_time:]
window_size = 10
batch_size = 16
shuffle_buffer_size = 1000

train_ds = windowed_dataset(train_open, window_size, batch_size, shuffle_buffer_size)

model = tf.keras.models.Sequential([
    Conv1D(filters=64, kernel_size=5, activation='relu', padding='causal',input_shape=[None, 1]),
    Bidirectional(LSTM(32, activation='relu', return_sequences=True)),
    Bidirectional(LSTM(32, activation='relu', return_sequences=True)),
    Dense(256, activation='relu'),
    Dense(1)
])

lr_schedule = tf.keras.callbacks.LearningRateScheduler(
    lambda epoch: 1e-8 * 10 ** (epoch/20)
)
#optimizer = tf.keras.optimizers.SGD(lr=1e-5, momentum=0.9)
optimizer = tf.keras.optimizers.Adam(lr=2e-4)
model.compile(metrics=['mae'], loss=tf.keras.losses.Huber(), optimizer=optimizer)
history = model.fit(train_ds, epochs=100)

#plt.semilogx(history.history['lr'], history.history['loss'])

epoch = range(len(history.history['loss']))
plt.plot(epoch[10:], history.history['mae'][10:])

#model.save('D:/Downloads/stockMtoM.h5')
#model = tf.keras.models.load_model('D:/Downloads/stockMtoM.h5')

rnn_forecast = model_forecast(model, open[..., np.newaxis], window_size)
rnn_forecast = rnn_forecast.reshape(1250, -1)

rnn_forecast_mean = np.mean(rnn_forecast, axis=-1)

rnn_forecast = rnn_forecast_mean[split_time - window_size:-1]

plt.figure(figsize=(10, 6))
plot_series(time_steps[split_time:], test_open, 'r')
plot_series(time_steps[split_time:], rnn_forecast, 'b')

tf.keras.metrics.mae(test_open,rnn_forecast).numpy()