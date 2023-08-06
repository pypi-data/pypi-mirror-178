import json
import random

import numpy as np
from tensorflow import keras
from sklearn.metrics import mean_squared_error


def evaluate_model(model_path, test_file_name, sequence_length,  num_examples=20, look_back_time_step=50):
    """
    Evaluates model by randomly selecting num_examples from test data.
    Prints rmse errors between label and prediction.

    :param model_path: relative path e.g 'trained_models/model_name'
    :param test_file_name: relative path e.g datasets/test_data.json
    :param num_examples: number of examples randomly selected to display in evaluation.
    :param sequence_length: select this based on the sequence length of test data.
    :param look_back_time_step: models have been trained with default value 50.
                                Only change this if model is trained with a different value than 50.
    """
    with open(test_file_name, "r") as json_file:
        test_data = json.load(json_file)
    test_labels = test_data.pop('sequence_labels')
    test_data = np.stack(
        [test_data['sequence_values'], test_data['sequence_masks']], axis=2)
    test_data = np.array(test_data)
    test_labels = np.array(test_labels)
    model = keras.models.load_model(model_path, custom_objects={'root_mean_squared_error_loss': None})
    num_features = int(sequence_length/look_back_time_step) * 2
    for _ in range(num_examples):
        index = random.choice(range(len(test_data)))
        label = test_labels[index]
        prediction = model.predict(test_data[index].reshape(1, look_back_time_step, num_features), verbose=0)[0][0]
        print(
            f'label: {label:.2f} , '
            f'prediction = {prediction:.2f}, '
            f'mse = {mean_squared_error([label], [prediction]):.5f}')


if __name__ == '__main__':
    _model_path = 'trained_models/rnn__sequence_length_600__lr_0.01__gc_100_examples_100k_epochs_30'
    _test_file_name = 'datasets/sequence_length_600__num_examples_10000_test_1_dp.json'
    evaluate_model(_model_path, _test_file_name, sequence_length=600)
