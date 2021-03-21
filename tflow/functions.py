import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import pandas as pd
pd.set_option("display.max_rows", None, "display.max_columns", None)

def plot_series(time, series, format="-", start=0, end=None):
    plt.plot(time[start:end], series[start:end], format)
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.grid(True)

def normalize(input,min=None, max=None):
    min = min if min is not None else np.min(input)
    max = max if max is not None else np.max(input)
    input -= min
    input /= max
    return input

def add_ema(input, col, min_max_long=None, min_max_short=None):
    return_df = pd.DataFrame({col: input[:, 0]})
    return_df[col+'_200dayEMA'] = return_df.iloc[:, 0].ewm(span=200, adjust=False).mean()
    return_df[col+'_50dayEMA'] = return_df.iloc[:, 0].ewm(span=50, adjust=False).mean()
    return_df[col+'_20dayEMA'] = return_df.iloc[:, 0].ewm(span=20, adjust=False).mean()
    return_df[col+'_short_term'] = return_df[col+'_20dayEMA'] - return_df[col+'_50dayEMA']
    return_df[col+'_long_term'] = return_df[col+'_50dayEMA'] - return_df[col+'_200dayEMA']
    if(min_max_long is None):
        return_df[col+'_long_term'] = normalize(return_df[col+'_long_term'])
        return_df[col+'_short_term'] = normalize(return_df[col+'_short_term'])
    else:
        return_df[col+'_long_term'] = normalize(return_df[col+'_long_term'], min_max_long[0],min_max_long[1])
        return_df[col+'_short_term'] = normalize(return_df[col+'_short_term'], min_max_short[0],min_max_short[1])
    return np.asarray(return_df)    


def windowed_dataset(series, window_size, batch_size, shuffle_buffer_size):
    #series = tf.expand_dims(series, axis=-1)# remvoed as the array reshaped to(-1,1) for concatenate
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size+1, shift=1,drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(window_size+1))
    ds = ds.shuffle(shuffle_buffer_size)
    ds = ds.map(lambda w: (w[:-1], w[-1][0]))
    return ds.batch(batch_size).prefetch(1)

def model_forecast(model, series, window_size):
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w:w.batch(window_size))
    ds = ds.batch(32).prefetch(1)
    forecast = model.predict(ds)
    return forecast