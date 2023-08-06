import pathlib
import json
import numpy as np
import tensorflow as tf
import pickle
import evaluate
from tensorflow import keras
from keras import backend as keras_backend
import keras_tuner as kt
from matplotlib import pyplot as plt
from pprint import pprint
from settings import *


class Train:
    def __init__(self, data_name_train, data_name_test, out_path, model_architecture='rnn', debug=False):
        """
        Main class for training model based on given train and test data and model architecture.
        :param data_name_train: name of train data found in /datasets directory
                                e.g. sequence_length_150__num_examples_100000_train_1_dp
        :param data_name_test: name of test data found in /datasets directory
                                e.g. sequence_length_150__num_examples_10000_test_1_dp
        :param model_architecture: specifies the type of architecture e.g. 'rnn' or 'lstm'. both use 100 hidden units.
        :param out_path: directory where the model should be stored.
        :param debug: if True then settings.num_examples_debug are used for training and testing instead of whole data.
        """
        self.data_name_train = data_name_train
        self.data_name_test = data_name_test
        self.training_parameters = None
        self.model_architecture = model_architecture
        self.out_path = out_path
        self.base_path = ''
        self.debug = debug
        self.train_data = None
        self.train_labels = None
        self.test_data = None
        self.test_labels = None
        self.model = None
        self.model_history = None
        self.optimizer=None
        self.loss=None

        self.run()

    def run(self):
        """ Main function that runs data preprocessing, training and evaluation. """
        self.preprocess()
        self.train()
        self.evaluate()

    def preprocess(self):
        """ Creates model directories, loads and preprocesses train and test data. """
        self.create_model_directory()
        self.load_train_and_test_data()
        self.preprocess_train_and_test_data()

    def train(self):
        """ Trains model and saves loss and metrics. """
        self.create_model()
        self.create_optimizer_and_loss()
        if tune_hyper_parameters:
            self.get_best_tuned_model()
        else:
            self.compile_model()
        self.fit_model()
        self.plot_model_history_curves()

    def evaluate(self):
        """
            Evaluates model on test data and prints average test loss and test rmse.
            Also prints predictions, labels and rmse of 20 randomly selected examples from test data.
        """
        test_loss, test_rmse = self.model.evaluate(self.test_data, self.test_labels)
        print(f'Test data loss: {test_loss}', f'\tTest data rmse: {test_rmse}')
        print('Result for prediction of 20 randomly selected examples from test data:')
        evaluate.evaluate_model(self.out_path, 'datasets/' + self.data_name_test + '.json', sequence_length)

    def create_model_directory(self):
        """
        Creates out_path directory where model is saved.
        model name is made up of model_type, sequence_length, num_examples_debug and number of epochs
        """
        self.base_path = self.out_path
        model_name = f'/{self.model_architecture}__sequence_length_{sequence_length}' \
                     + f'__examples_{num_examples_debug if self.debug else "100k"}_epochs_{epochs}' + \
                     ('_debug' if self.debug else '') + \
                     (f'_{model_name_suffix}' if len(model_name_suffix) > 0 else '')
        if tune_hyper_parameters:
            self.out_path += f'/keras_tuner/best_tuned_model/{self.model_architecture}_params_tuning'
            if self.debug:
                self.out_path += f'_debug_{num_examples_debug}_examples'
        else:
            self.out_path += model_name
        pathlib.Path(self.out_path).mkdir(exist_ok=True, parents=True)

    def load_train_and_test_data(self):
        """
        Loads train and test data specified in self.data_name_train and self.data_name_test
        """
        train_data_file_name = 'datasets/' + self.data_name_train + '.json'
        with open(train_data_file_name, "r") as json_file:
            self.train_data = json.load(json_file)
        self.train_data = {key: values[:num_examples_debug if self.debug else None]
                           for key, values in self.train_data.items()}
        self.train_labels = self.train_data.pop('sequence_labels')

        test_data_file_name = 'datasets/' + self.data_name_test + '.json'
        with open(test_data_file_name, "r") as json_file:
            self.test_data = json.load(json_file)
        self.test_data = {key: values[:num_examples_debug if self.debug else None]
                          for key, values in self.test_data.items()}
        self.test_labels = self.test_data.pop('sequence_labels')

    def preprocess_train_and_test_data(self):
        """
        Preprocesses train and test data and reshapes it in a format that is expected by sequential model.
        """
        self.train_data = np.stack([self.train_data['sequence_values'], self.train_data['sequence_masks']], axis=2)
        self.test_data = np.stack([self.test_data['sequence_values'], self.test_data['sequence_masks']], axis=2)

        self.train_data = np.array(self.train_data)
        self.train_labels = np.array(self.train_labels)
        self.test_data = np.array(self.test_data)
        self.test_labels = np.array(self.test_labels)

        # reshaping train and test data for sequential model. 100k train samples and 10k test samples
        self.train_data = self.train_data.reshape((100000, look_back_time_steps, num_features))
        self.test_data = self.test_data.reshape((10000, look_back_time_steps, num_features))

    def create_model(self):
        """
        Creates model based on self.model_architecture
        """
        model = keras.Sequential()
        if self.model_architecture == 'rnn':
            model.add(keras.layers.InputLayer(input_shape=(look_back_time_steps, num_features)))
            model.add(
                keras.layers.SimpleRNN(100, activation='relu', recurrent_initializer=keras.initializers.identity,
                                       kernel_initializer=keras.initializers.truncated_normal(mean=0, stddev=0.001))),
        elif self.model_architecture == 'lstm':
            model.add(keras.layers.LSTM(100))
        model.add(keras.layers.Dense(1, activation='relu'))
        self.model = model

    def create_optimizer_and_loss(self):
        """ Creates optimizer and loss based on values specified in settings.py. """
        if optimizer == 'sgd':
            self.optimizer = keras.optimizers.SGD(learning_rate=learning_rate, clipvalue=gradient_clipping_value)
        elif optimizer == 'rmsprop':
            self.optimizer = 'rmsprop'

        if loss == 'root_mean_squared_error_loss':
            self.loss = Train.root_mean_squared_error_loss
        elif loss == 'mean_squared_error_loss':
            self.loss = keras.losses.mean_squared_error

    def compile_model(self):
        """ Compiles model based on loss and optimizer specified in settings.py """
        self.model.compile(optimizer=self.optimizer, metrics=[keras.metrics.MeanSquaredError()], loss=self.loss)

    def get_best_tuned_model(self):
        """ Finds best learning rate and gradient clip value for 'sgd' optimizer and creates best model"""
        tuner = kt.Hyperband(
            self.build_tuner_model,
            objective=objective,
            max_epochs=max_tuner_epochs,
            directory=self.base_path,
            project_name=self.out_path

        )
        tuner.search(self.train_data, self.train_labels, batch_size=batch_size,
                     validation_data=(self.test_data, self.test_labels))
        tuner.results_summary()
        print('****** BEST PARAMS ******')
        pprint(tuner.get_best_hyperparameters()[0].values)
        self.model = tuner.get_best_models()[0]

    def build_tuner_model(self, hp):
        """ builds tuner model using learning_rate_list, gradient_clipping_values_list and momentum in settings.py """
        hp_learning_rate = hp.Choice('learning_rate', values=learning_rate_list)
        hp_momentum = hp.Choice('momentum', values=momentum)
        if self.optimizer == 'rmsprop':
            _optimizer = keras.optimizers.RMSprop(learning_rate=hp_learning_rate, momentum=hp_momentum)
        else:
            hp_gradient_clipping_value = hp.Choice('clipvalue', values=gradient_clipping_values_list)
            _optimizer = keras.optimizers.SGD(learning_rate=hp_learning_rate, clipvalue=hp_gradient_clipping_value)
        self.model.compile(
            optimizer=_optimizer,
            metrics=[keras.metrics.MeanSquaredError()],
            loss=self.loss
        )
        return self.model

    def fit_model(self):
        """ Trains model and saves statistics like validation loss and mean squared error on train and test data."""
        self.model.build(input_shape=(look_back_time_steps, num_features))
        self.model.summary()
        with tf.device('/gpu:0'):
            self.model_history = \
                self.model.fit(self.train_data, self.train_labels, epochs=epochs, batch_size=batch_size,
                               validation_data=(self.test_data, self.test_labels))
            self.model.save(self.out_path)
            with open(self.out_path + '/model_history', 'wb') as file:
                pickle.dump(self.model_history.history, file)

    def plot_model_history_curves(self):
        """ Plots losses and mean squared errors for train and test data. """
        plt.plot(self.model_history.history['mean_squared_error'])
        plt.plot(self.model_history.history['val_mean_squared_error'])
        plt.plot([0.1767] * len(self.model_history.history['mean_squared_error']))  # baseline MSE
        plt.ylim((0.0, 0.8))
        plt.title(f'MSE vs Epochs (sequence length: {sequence_length})')
        plt.ylabel('MSE')
        plt.xlabel('epoch')
        plt.legend(['train MSE', 'val MSE', 'baseline MSE'], loc='upper left')
        plt.savefig(self.out_path + '/MSE.png')
        plt.clf()

        plt.plot(self.model_history.history['loss'])
        plt.plot(self.model_history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'val'], loc='upper left')
        plt.savefig(self.out_path + '/loss.png')

    @staticmethod
    def root_mean_squared_error_loss(y_label, y_prediction):
        """ Implements custom root mean squared error loss. """
        return keras_backend.sqrt(keras_backend.mean(keras_backend.square(y_prediction - y_label)))


if __name__ == '__main__':
    # Please make sure that sequence_length in settings.py is set correctly to the sequence length used in data.
    _data_name_train = 'sequence_length_600__num_examples_100000_train_1_dp'
    _data_name_test = 'sequence_length_600__num_examples_10000_test_1_dp'
    _out_path = f'D:/MyData/ml_code/dl-keras/trained_models'
    Train(_data_name_train, _data_name_test, _out_path)
