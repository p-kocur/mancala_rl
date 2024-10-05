import numpy as np
import tensorflow as tf
import keras


def make_cnn():
    model = keras.models.Sequential()
    model.add(keras.Input(shape=(2, 6, 1)))