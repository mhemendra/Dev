import os
from datetime import datetime
import pandas as pd
#Below runs the code on CPU
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
pd.set_option("display.max_rows", None, "display.max_columns", None)

import csv
from tflow.functions import *

start_time = datetime.now()
close_price = []
volume=[]
split_time = 4000

time_steps=[]
index = 0
with open(r'D:/Downloads/500790.csv') as file:
    csv_reader = csv.reader(file, delimiter=',')
    next(csv_reader)
    #sel_rows = [row for idx, row in enumerate(csv_reader) if idx>2]
    for row in csv_reader:
        index +=1
        time_steps.append(index)
        close_price.append(float(row[4]))# If float not added then order missing in plots as its string
        volume.append(float(row[6]))

time_steps = np.array(time_steps)
close_price = np.array(close_price).reshape(-1, 1)
#volume = np.array(volume).reshape(-1, 1)
#volume = normalize(volume)
close_price = normalize(close_price)
test_close = close_price[split_time:]# Moved here so that EMA not present in this df and this is used only for mae

close_price = add_ema(close_price, 'close_price')
#open_df = open_df.drop(['200dayEMA','50dayEMA','20dayEMA'], axis=1)
#plt.figure(figsize=(10,6))
#plot_series(time_steps, open, start=6000)
totalVars = close_price.shape[1]
train_volume = volume[:split_time]
train_close = close_price[:split_time]

#train_data = np.concatenate([train_close, train_volume], axis=1)
train_data = np.concatenate([train_close], axis=1)

#totalVars+=1
window_size = 10
batch_size = 16
shuffle_buffer_size = 1000

train_ds = windowed_dataset(train_data, window_size, batch_size, shuffle_buffer_size)

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv1D(filters=64, kernel_size=5, activation='relu', padding='causal',input_shape=[None, totalVars]),
    tf.keras.layers.LSTM(128, activation='relu', return_sequences=True),
    tf.keras.layers.LSTM(128, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(metrics=['mae'], loss=tf.keras.losses.Huber(), optimizer='adam')
#history = model.fit(train_ds, epochs=50)
#model.save('stockMulti.h5')

model = tf.keras.models.load_model('stockMulti.h5')
#add +1 to loop if the last value is to be taken and predict the next totally new value

#Using the close price as inputs
"""rnn_forecast = []
for time in range(split_time-window_size, (len(close_price) - window_size)):
    input = close_price[time:time + window_size].reshape(-1,window_size,totalVars)
    pred_out = model.predict(input)
    rnn_forecast = np.append(rnn_forecast, pred_out)
rnn_forecast = rnn_forecast.reshape(-1,1)
forecast = np.array(rnn_forecast)[:, 0]"""

#Calculating EMA for predicted out
rnn_forecast = close_price[:, 0][split_time - window_size:split_time]
train_open_conc = close_price[:,0][:split_time-window_size].reshape(-1,1)
#test_volume = volume[split_time - window_size:]
for time in range((len(close_price) - split_time)):
    close_ema = add_ema(np.concatenate([train_open_conc, rnn_forecast.reshape(-1,1)],axis=0), 'close_price')
    close_test = close_ema[split_time+time-window_size:split_time+time].reshape(-1, totalVars)# 1 added for volume so removed here
    input = close_test.reshape(-1, window_size, totalVars)
    #vol_test = test_volume[time:time + window_size]
    #input = np.concatenate([close_test, vol_test], axis=1).reshape(-1, window_size, totalVars)
    pred_out = model.predict(input)
    rnn_forecast = np.append(rnn_forecast, pred_out)
rnn_forecast = rnn_forecast[window_size:].reshape(-1,1)
forecast = np.array(rnn_forecast)[:, 0]

#Original without Volume
"""rnn_forecast = close_price[:, 0][split_time - window_size:split_time]
close_price_ema = close_price[:, 1:][split_time - window_size:]
test_volume = volume[split_time - window_size:]
for time in range((len(close_price) - split_time)):
    close_test = rnn_forecast[time:time + window_size].reshape(-1,1)
    vol_test = test_volume[time:time + window_size]
    close_price_ema_input = close_price_ema[time:time + window_size]
    input = np.concatenate([close_test, close_price_ema_input], axis=1).reshape(-1, window_size, totalVars)
    break
    pred_out = model.predict(input)
    rnn_forecast = np.append(rnn_forecast, pred_out)
rnn_forecast = rnn_forecast[window_size:].reshape(-1,1)
forecast = np.array(rnn_forecast)[:, 0]"""

mae = tf.keras.metrics.mae(test_close.reshape(-1), forecast).numpy()
print("mae::",mae)
end_time = datetime.now()
print("time_taken",end_time-start_time)

"""plt.figure(figsize=(10, 6))
plot_series(time_steps[split_time:], test_close, 'r')
plot_series(time_steps[split_time:], forecast, 'y')"""