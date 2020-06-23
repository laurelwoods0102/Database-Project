import numpy as np
from tensorflow import keras
from query import QueryProcess


city = "Gangnam-gu"
category = "Beer"

query_process = QueryProcess()
data_2018 = query_process.query_dataset(2018, city, category)

test_data = data_2018.tail(32)
test_data = np.array([test_data.values[:, :15]])

new_model = keras.models.load_model('model_Gangnam-gu_Beer.h5')
new_model.summary()


normalize_info = np.genfromtxt("{0}_{1}_normalize.csv".format(city, category), delimiter=",")

print(new_model.predict(test_data)*normalize_info[1] + normalize_info[0])
