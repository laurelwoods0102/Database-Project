import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from pprint import pprint

from query import QueryProcess

class Preprocess:
    def __init__(self, TRAIN_SPLIT, TEST_SPLIT, PAST_HISTORY, FUTURE_TARGET, BATCH_SIZE, EPOCHS):
        self.train_split = TRAIN_SPLIT
        self.test_split = TEST_SPLIT
        self.past_history = PAST_HISTORY
        self.future_target = FUTURE_TARGET
        self.batch_size = BATCH_SIZE
        self.epochs = EPOCHS
    



# Normalization
def normalize(data):
    mean = data.mean(axis=0)
    std = data.std(axis=0)

    dataset = (data - mean)/std
    return dataset, mean, std

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

def plot_train_history(history, title, neuron_1=None, neuron_2=None):
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(len(loss))

    plt.figure()

    plt.plot(epochs, loss, 'b', label='Training loss')
    plt.plot(epochs, val_loss, 'r', label='Validation loss')
    plt.title(title)
    plt.legend()

    #plt.show()
    #plt.savefig("./results/loss_{}-{}.png".format(neuron_1, neuron_2), dpi=300)

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

if __name__ == "__main__":
    # Parameters
    TRAIN_SPLIT = 500      
    TEST_SPLIT = 64
    PAST_HISTORY = 32
    FUTURE_TARGET = 32
    BATCH_SIZE = 256
    EPOCHS = 20
    SEED = 13
    BUFFER_SIZE = 50000

    city = "Gangnam-gu"
    category = "Beer"

    query_process = QueryProcess()
    data_2017 = query_process.query_dataset(2017, city, category)
    data_2018 = query_process.query_dataset(2018, city, category)
    
    data = pd.concat([data_2017, data_2018]).values
    features = data[:, :15]
    label = data[:, -1:]
    
    dataset, _, _ = normalize(features)
    label, mean, std = normalize(label)

    np.savetxt("{0}_{1}_normalize.csv".format(city, category), np.array([mean[0], std[0]]), delimiter=",")

    #x_train_multi, y_train_multi = multivariate_data(dataset[:, :15], dataset[:, -1], 0,TRAIN_SPLIT, PAST_HISTORY, FUTURE_TARGET)
    #x_val_multi, y_val_multi = multivariate_data(dataset[:, :15], dataset[:, -1],TRAIN_SPLIT, None, PAST_HISTORY, FUTURE_TARGET)
    x_train_multi, y_train_multi = multivariate_data(features, label, 0, TRAIN_SPLIT, PAST_HISTORY, FUTURE_TARGET)
    x_val_multi, y_val_multi = multivariate_data(features, label, TRAIN_SPLIT, None, PAST_HISTORY, FUTURE_TARGET)

    
    #print ('Single window of past history : {}'.format(x_train_multi[0].shape))
    #print ('\n Target Sales to predict : {}'.format(y_train_multi[0].shape))

    train_data_multi = tf.data.Dataset.from_tensor_slices((x_train_multi, y_train_multi))
    train_data_multi = train_data_multi.cache().shuffle(BUFFER_SIZE).batch(BATCH_SIZE).repeat()

    val_data_multi = tf.data.Dataset.from_tensor_slices((x_val_multi, y_val_multi))
    val_data_multi = val_data_multi.batch(BATCH_SIZE).repeat()

    #for x, y in train_data_multi.take(2):
    #   multi_step_plot(x[0], y[0], np.array([0]))
    
    num_neurons_1 = 40
    num_neurons_2 = 16

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.LSTM(num_neurons_1, return_sequences=True, input_shape=x_train_multi.shape[1:]))
    model.add(tf.keras.layers.LSTM(num_neurons_2, activation='relu'))
    model.add(tf.keras.layers.Dense(32))

    model.compile(optimizer=tf.keras.optimizers.RMSprop(clipvalue=1.0), loss='mae')
    #model.compile(optimizer=tf.keras.optimizers.Adam(), loss='mae')

    model.fit(train_data_multi, epochs=EPOCHS, steps_per_epoch=BATCH_SIZE, validation_data=val_data_multi, validation_steps=50)
    #preprocess.plot_train_history(multi_step_history, 'Multi-Step Training and validation loss', num_neurons_1, num_neurons_2)
    model.save("model_{0}_{1}.h5".format(city, category))

    #for x, y in val_data_multi.take(1):
    #    print (multi_step_model.predict(x).shape)
    
    #for x, y in val_data_multi.take(2):
    #    multi_step_plot(x[0], y[0], multi_step_model.predict(x)[0])
