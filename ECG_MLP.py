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

# Define model for estimate
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

# Transfor tensfor to numpy
train_data=np.array(train_data)
test_data=np.array(test_data)

# MLP

# Params_dict
params = dict(learning_rate=[0.1,0.01,0.001],epochs=[10,20,30],batch_size=[8,32,64],activation=['relu','tanh'],nn=[16,32,64],nl=[2,4,6])

# Make a general model 
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

# Build MLP architecture
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

# Train model
hist_mlp = MLP.fit(train_data,train_labels,validation_split=0.2,epochs=30,batch_size=64,callbacks=[monitor_val_loss])

# Plot loss curve
plot_loss(hist_mlp.history['loss'], hist_mlp.history['val_loss'])

# Show test result
MLP.evaluate(test_data,test_labels)

# Predict and mark
y_pred_mlp=MLP.predict_classes(test_data)
print(f1_score(test_labels, y_pred_mlp, average="macro"))
print(precision_score(test_labels, y_pred_mlp, average="macro"))
print(recall_score(test_labels, y_pred_mlp, average="macro"))



"""### Plot val_loss and vol_acc plot"""

plt.figure()
plt.plot(hist_mlp.history['val_loss'])
#plt.plot(hist_cnn.history['val_loss'])
#plt.plot(hist_lstm.history['val_loss'])
plt.title('Model val_loss')
plt.ylabel('val_loss')
plt.xlabel('Epoch')
plt.legend(['mlp'], loc='upper right')
#plt.legend(['mlp', 'cnn','lstm'], loc='upper right')

plt.show()

plt.figure()
plt.plot(hist_mlp.history['val_accuracy'])
#plt.plot(hist_cnn.history['val_accuracy'])
#plt.plot(hist_lstm.history['val_accuracy'])
plt.title('Model val_accuracy')
plt.ylabel('val_accuracy')
plt.xlabel('Epoch')
plt.legend(['mlp'], loc='upper right')
#plt.legend(['mlp', 'cnn','lstm'], loc='upper right')

plt.show()
