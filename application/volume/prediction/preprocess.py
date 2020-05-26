import numpy as np
import pandas as pd
import json
import datetime

import tensorflow as tf

TRAIN_SPLIT = 1004      # Train 2016/01/01 ~ 2018/09/30
TEST_SPLIT = 61         # Test 2018/10/01 ~ 2018/11/31
PAST_HISTORY = 30       # Train last 30 days 
FUTURE_TARGET = 7       # Predict for next 7 days
STEP = 1                # 1 data = 1 days


def multivariate_data(dataset, target, start_index, end_index, history_size, target_size, step, single_step=False):
    data = []
    labels = []

    start_index = start_index + history_size
    if end_index is None:
        end_index = len(dataset) - target_size

    for i in range(start_index, end_index):
        indices = range(i-history_size, i, step)
        data.append(dataset[indices])

    if single_step:
        labels.append(target[i+target_size])
    else:
        labels.append(target[i:i+target_size])

    return np.array(data), np.array(labels)

x_train_multi, y_train_multi = multivariate_data(dataset, dataset[:, 1], 0, TRAIN_SPLIT, past_history, future_target, STEP)
x_val_multi, y_val_multi = multivariate_data(dataset, dataset[:, 1], TRAIN_SPLIT, None, past_history, future_target, STEP)