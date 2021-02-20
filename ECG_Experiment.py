# -*- coding: utf-8 -*-
"""ECG_Experiment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LeOZXR-ubev-IXBGUkuyFpSwPotqvNk6

### Import ECG Data
"""

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

# Download the dataset
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

#plot function to show the loss_curve of history 
def plot_loss(loss,val_loss):
  plt.figure()
  plt.plot(loss)
  plt.plot(val_loss)
  plt.title('Model loss')
  plt.ylabel('Loss')
  plt.xlabel('Epoch')
  plt.legend(['Train', 'Test'], loc='upper right')
  plt.show()

# earlyStopping function to end epcho
monitor_val_loss = EarlyStopping(monitor='val_loss', patience=3)

# define model for estimate
def create_model (learning_rate, activation, nl, nn):
  opt = Adam(lr = learning_rate)
  model = Sequential()
  model.add(Dense(32,input_shape=(140,),activation=activation))
  for i in range(nl):
    model.add(Dense(nn,activation=activation))
  model.add(Dense(1,activation='sigmoid'))
  model.compile(optimizer=opt, loss='binary_crossentropy',metrics=['accuracy'])
  return model

"""### Use MLP method to model"""

from keras.models  import Sequential
from keras.optimizers import Adam
from keras.layers import Dense,BatchNormalization
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import RandomizedSearchCV, KFold

# transfor tensfor to numpy
train_data=np.array(train_data)
test_data=np.array(test_data)

# MLP

# params_dict
params = dict(learning_rate=[0.1,0.01,0.001],epochs=[10,20,30],batch_size=[8,32,64],activation=['relu','tanh'],nn=[16,32,64],nl=[2,4,6])

# make a general model 
model = KerasClassifier(build_fn=create_model)
random_search = RandomizedSearchCV(model,params,cv=2)

"""
# fit(X,Y) taks too long. Only show result here
random_search_result = random_search.fit(train_data,train_labels)
print(random_search.best_score_)
print(random_search.best_params_)

# below is result from random_search.fit()
#best_score0.9844922423362732
#best_params='nn': 64, 'nl': 4, 'learning_rate': 0.001, 'epochs': 30, 'batch_size': 64, 'activation': 'tanh'}
"""

# build MLP architecture
opt = Adam(lr = 0.001)
MLP = Sequential()
MLP.add(Dense(32,input_shape=(140,),activation='tanh'))
MLP.add(Dense(64,activation='tanh'))
MLP.add(Dense(64,activation='tanh'))
MLP.add(Dense(64,activation='tanh'))
MLP.add(Dense(64,activation='tanh'))
MLP.add(Dense(1,activation='sigmoid'))
MLP.compile(optimizer=opt, loss='binary_crossentropy',metrics=['accuracy'])
MLP.summary()

# train model
hist_mlp = MLP.fit(train_data,train_labels,validation_split=0.2,epochs=30,batch_size=64,callbacks=[monitor_val_loss])

# plot loss curve
plot_loss(hist_mlp.history['loss'], hist_mlp.history['val_loss'])

# show test result
MLP.evaluate(test_data,test_labels)

# predict and mark
y_pred_mlp=MLP.predict_classes(test_data)
print(f1_score(test_labels, y_pred_mlp, average="macro"))
print(precision_score(test_labels, y_pred_mlp, average="macro"))
print(recall_score(test_labels, y_pred_mlp, average="macro"))

"""###Use CNN method to model"""

# conv1D

from keras.layers import Conv1D,MaxPooling1D

# transform into suitable shape
train_data_cnn = train_data.reshape(-1, 140, 1)
test_data_cnn = test_data.reshape(-1, 140, 1)


# build CNN architecture
CNN = Sequential()
CNN.add(Conv1D(16, 10, activation='tanh', input_shape=(140,1)))
CNN.add(Conv1D(16, 10, activation='tanh'))
CNN.add(MaxPooling1D(3))
CNN.add(Dropout(0.25))
CNN.add(Conv1D(32, 10, activation='tanh'))
CNN.add(Conv1D(32, 10, activation='tanh'))
CNN.add(MaxPooling1D(3))
CNN.add(Dropout(0.25))

CNN.add(Flatten())

CNN.add(Dense(128,activation='tanh'))
CNN.add(Dropout(0.25))
CNN.add(Dense(1, activation='sigmoid'))
CNN.summary()

CNN.compile(loss='binary_crossentropy', metrics=['accuracy'], optimizer=opt)

hist_cnn = CNN.fit(train_data_cnn,train_labels, batch_size=14, epochs=50, validation_split=0.2, callbacks=[monitor_val_loss])

# plot loss curve
plot_loss(hist_cnn.history['loss'], hist_cnn.history['val_loss'])

# show test result
CNN.evaluate(test_data_cnn,test_labels)

# predict and mark
y_pred_cnn=CNN.predict_classes(test_data_cnn)
print(f1_score(test_labels, y_pred_cnn, average="macro"))
print(precision_score(test_labels, y_pred_cnn, average="macro"))
print(recall_score(test_labels, y_pred_cnn, average="macro"))

"""### Use LSTM method to model """

from keras.layers import LSTM, Embedding
from keras.preprocessing import sequence, text


# transform into suitable shape
train_data_lstm = train_data.reshape((train_data_0.shape[0], train_data_0.shape[1], 1))
test_data_lstm = test_data.reshape((test_data_0.shape[0], test_data_0.shape[1], 1))

# build LSTM architecture
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

# plot loss curve
plot_loss(hist_lstm.history['loss'], hist_lstm.history['val_loss'])
#test_data = test_data_0.reshape((test_data_0.shape[0], test_data_0.shape[1], 1))
# show test result
Lstm.evaluate(test_data_lstm,test_labels)

# predict and mark
y_pred_lstm=Lstm.predict_classes(test_data_lstm)
print(f1_score(test_labels, y_pred_lstm, average="macro"))
print(precision_score(test_labels, y_pred_lstm, average="macro"))
print(recall_score(test_labels, y_pred_lstm, average="macro"))


# plot val_loss and vol_acc plot
plt.figure()
plt.plot(hist_mlp.history['val_loss'])
plt.plot(hist_cnn.history['val_loss'])
plt.plot(hist_lstm.history['val_loss'])
plt.title('Model val_loss')
plt.ylabel('val_loss')
plt.xlabel('Epoch')
plt.legend(['mlp', 'cnn','lstm'], loc='upper right')
plt.show()

plt.figure()
plt.plot(hist_mlp.history['val_accuracy'])
plt.plot(hist_cnn.history['val_accuracy'])
plt.plot(hist_lstm.history['val_accuracy'])
plt.title('Model val_accuracy')
plt.ylabel('val_accuracy')
plt.xlabel('Epoch')
plt.legend(['mlp', 'cnn','lstm'], loc='upper right')
plt.show()
