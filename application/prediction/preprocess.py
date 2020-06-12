import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from pprint import pprint

from query import QueryProcess

class Preprocess:
    def __init__(self, DATA, TRAIN_SPLIT, TEST_SPLIT, PAST_HISTORY, FUTURE_TARGET, BATCH_SIZE, EVALUATION_INTERVAL, EPOCHS, SEED):
        self.train_split = TRAIN_SPLIT
        self.test_split = TEST_SPLIT
        self.past_history = PAST_HISTORY
        self.future_target = FUTURE_TARGET
        self.batch_size = BATCH_SIZE
        self.evaluation_interval = EVALUATION_INTERVAL
        self.epochs = EPOCHS
        self.seed = SEED
    
    def normalization(self):    # Normalization
        train_mean = self.data.mean()
        train_std = self.data.std()

        self.dataset = (self.data - train_mean)/train_std
        
        return train_mean, train_std

def multivariate_data(dataset, target, start_index, end_index, history_size, target_size):
    data = []
    labels = []

    start_index = start_index + history_size
    if end_index is None:
        end_index = len(dataset) - target_size

    for i in range(start_index, end_index):
        indices = range(i-history_size, i)
        data.append(dataset[indices])

        labels.append(target[i:i+target_size])

    return np.array(data), np.array(labels)

def create_time_steps(length):
    return list(range(-length, 0))

def multi_step_plot(history, true_future, prediction):
    plt.figure(figsize=(12, 6))
    num_in = create_time_steps(len(history))
    num_out = len(true_future)

    plt.plot(num_in, np.array(history[:, 1]), label='History')
    plt.plot(np.arange(num_out), np.array(true_future), 'bo', label='True Future')

    if prediction.any():
        plt.plot(np.arange(num_out), np.array(prediction), 'ro', label='Predicted Future')

    plt.legend(loc='upper left')
    plt.show()
    #plt.savefig('val.png', dpi=300)

def plot_train_history(history, title):
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(len(loss))

    plt.figure()

    plt.plot(epochs, loss, 'b', label='Training loss')
    plt.plot(epochs, val_loss, 'r', label='Validation loss')
    plt.title(title)
    plt.legend()

    plt.show()

if __name__ == "__main__":
    # Parameters
    TRAIN_SPLIT = 500
    TEST_SPLIT = 100
    PAST_HISTORY = 32
    FUTURE_TARGET = 32
    BATCH_SIZE = 256
    EPOCHS = 20
    SEED = 13
    BUFFER_SIZE = 50000

    query_process = QueryProcess()
    data_2017 = query_process.query_dataset(2017, "Gangnam-gu", "Beer")
    data_2018 = query_process.query_dataset(2018, "Gangnam-gu", "Beer")
    
    data = pd.concat([data_2017, data_2018])
    
    #pprint(data.isnull().values.any())

    dataset = data.values
    data_mean = dataset[:TRAIN_SPLIT].mean(axis=0)
    data_std = dataset[:TRAIN_SPLIT].std(axis=0)

    dataset = (dataset-data_mean)/data_std

    x_train_multi, y_train_multi = multivariate_data(dataset[:, :15], dataset[:, -1], 0,TRAIN_SPLIT, PAST_HISTORY, FUTURE_TARGET)
    x_val_multi, y_val_multi = multivariate_data(dataset[:, :15], dataset[:, -1],TRAIN_SPLIT, None, PAST_HISTORY, FUTURE_TARGET)

    #print ('Single window of past history : {}'.format(x_train_multi[0].shape))
    #print ('\n Target Sales to predict : {}'.format(y_train_multi[0].shape))

    train_data_multi = tf.data.Dataset.from_tensor_slices((x_train_multi, y_train_multi))
    train_data_multi = train_data_multi.cache().shuffle(BUFFER_SIZE).batch(BATCH_SIZE).repeat()

    val_data_multi = tf.data.Dataset.from_tensor_slices((x_val_multi, y_val_multi))
    val_data_multi = val_data_multi.batch(BATCH_SIZE).repeat()

    #for x, y in train_data_multi.take(2):
    #   multi_step_plot(x[0], y[0], np.array([0]))

    multi_step_model = tf.keras.models.Sequential()
    multi_step_model.add(tf.keras.layers.LSTM(32, return_sequences=True, input_shape=x_train_multi.shape[1:]))
    multi_step_model.add(tf.keras.layers.LSTM(16, activation='relu'))
    multi_step_model.add(tf.keras.layers.Dense(32))

    multi_step_model.compile(optimizer=tf.keras.optimizers.RMSprop(clipvalue=1.0), loss='mae')

    #for x, y in val_data_multi.take(1):
    #    print (multi_step_model.predict(x).shape)
    
    multi_step_history = multi_step_model.fit(train_data_multi, epochs=EPOCHS, steps_per_epoch=BATCH_SIZE, validation_data=val_data_multi, validation_steps=50)
    plot_train_history(multi_step_history, 'Multi-Step Training and validation loss')

    for x, y in val_data_multi.take(2):
        multi_step_plot(x[0], y[0], multi_step_model.predict(x)[0])