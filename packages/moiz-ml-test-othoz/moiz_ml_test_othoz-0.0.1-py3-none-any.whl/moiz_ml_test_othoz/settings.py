# parameters for formatting input train and test data
sequence_length = 600                       # change it based on sequence length in input data
look_back_time_steps = 50                   # model looks back at these many samples in a sequence (do not change)
num_features = int(sequence_length/look_back_time_steps) * 2    # used for formatting input data to be fed in the model


# optimizer can be chosen from ['sgd', 'rmsprop']
# if 'sgd' is selected then learning_rate and gradient_clipping_value are used, 'rmsprop' uses only default values
learning_rate = 0.01
gradient_clipping_value = 100
optimizer = 'rmsprop'


num_examples_debug = 10000                              # number of examples to use when running in debug mode
batch_size = 150                                        # batch size used for the model
epochs = 30                                             # epochs used for training
loss = 'root_mean_squared_error_loss'                   # ['root_mean_squared_error_loss', 'mean_squared_error_loss']


# If tune_hyper_parameters is True then automatically tunes optimizer for given values.
# 'rmsprop' optimizer does not use gradient clip values when tuning.
# Automatically trains the model using the best hyperparameters found from values listed below.
# 'objective' for tuning is set to minimize validation loss.
tune_hyper_parameters = False
gradient_clipping_values_list = [1, 10, 100, 1000]
learning_rate_list = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9]
momentum = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
max_tuner_epochs = 30                                   # number of epochs to be used when tuning for best model.
objective = 'val_loss'                                  # objective used for finding best tuned hyperparameters.


model_name_suffix = ''                                  # added to the end of model name (optional)
