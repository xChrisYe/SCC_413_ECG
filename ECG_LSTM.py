# -*- coding: utf-8 -*-
"""ECG_Experiment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LeOZXR-ubev-IXBGUkuyFpSwPotqvNk6

"""

"""### Download and import the dataset """

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
np.random.seed(0)
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, losses
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.models import Model
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix



dataframe = pd.read_csv('http://storage.googleapis.com/download.tensorflow.org/data/ecg.csv', header=None)
raw_data = dataframe.values
dataframe.head()

# The last element contains the labels
labels = raw_data[:, -1]

# The other data points are the electrocadriogram data
data = raw_data[:, 0:-1]

train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size=0.2, random_state=21)

# Normalize to [0, 1]
min_val = tf.reduce_min(train_data)
max_val = tf.reduce_max(train_data)

train_data = (train_data - min_val) / (max_val - min_val)
test_data = (test_data - min_val) / (max_val - min_val)

train_data = tf.cast(train_data, tf.float32)
test_data = tf.cast(test_data, tf.float32)


from keras.callbacks import EarlyStopping

# Plot function to show the loss_curve of history 
def plot_loss(loss,val_loss):
  plt.figure()
  plt.plot(loss)
  plt.plot(val_loss)
  plt.title('Model loss')
  plt.ylabel('Loss')
  plt.xlabel('Epoch')
  plt.legend(['Train', 'Test'], loc='upper right')
  plt.show()

# EarlyStopping function to end epcho
monitor_val_loss = EarlyStopping(monitor='val_loss', patience=3)



"""### Use LSTM method to model """

from keras.layers import LSTM, Embedding
from keras.preprocessing import sequence, text


# Transform into suitable shape
train_data_lstm = train_data.reshape((train_data.shape[0], train_data.shape[1], 1))
test_data_lstm = test_data.reshape((test_data.shape[0], test_data.shape[1], 1))

# Build LSTM architecture
opt = Adam(lr = 0.001)
Lstm = Sequential()
Lstm.add(LSTM(units=50, activation='tanh', return_sequences=True, input_shape=(140,1)))
Lstm.add(Dropout(0.2))
Lstm.add(LSTM(units=50, activation='tanh', return_sequences=False))
Lstm.add(Dropout(0.2))
Lstm.add(Dense(1, activation='sigmoid'))

Lstm.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
Lstm.summary()


hist_lstm = Lstm.fit(train_data_lstm, train_labels, batch_size=80, validation_split = 0.2, epochs=50, shuffle=False, verbose=1,callbacks=[monitor_val_loss])

# Plot loss curve
plot_loss(hist_lstm.history['loss'], hist_lstm.history['val_loss'])
#test_data = test_data_0.reshape((test_data_0.shape[0], test_data_0.shape[1], 1))
# show test result
Lstm.evaluate(test_data_lstm,test_labels)

# Predict and mark
y_pred_lstm=Lstm.predict_classes(test_data_lstm)
print(f1_score(test_labels, y_pred_lstm, average="macro"))
print(precision_score(test_labels, y_pred_lstm, average="macro"))
print(recall_score(test_labels, y_pred_lstm, average="macro"))


"""### Plot val_loss and vol_acc plot"""

plt.figure()

plt.plot(hist_lstm.history['val_loss'])
plt.title('Model val_loss')
plt.ylabel('val_loss')
plt.xlabel('Epoch')
plt.legend(['lstm'], loc='upper right')
plt.show()

plt.figure()

plt.plot(hist_lstm.history['val_accuracy'])
plt.title('Model val_accuracy')
plt.ylabel('val_accuracy')
plt.xlabel('Epoch')
plt.legend(['lstm'], loc='upper right')
plt.show()