import pathlib
import random
import numpy as np
import json
from random import randrange
from sys import stdout


class GenerateData(object):
    def __init__(self, out_path, sequence_length=20, num_examples=1000, number_of_decimal_places=4, mode='train'):
        self.out_path = out_path
        self.sequence_length = sequence_length
        self.num_examples = num_examples
        self.number_of_decimal_places = number_of_decimal_places
        self.mode = mode
        self.data = []

        self.generate_examples()
        self.write_data_to_json()

    def generate_examples(self):
        for _ in range(self.num_examples):
            self.data.append(self.generate_example())
            stdout.write(f'\rGenerated examples: {len(self.data)}/{self.num_examples}, '
                         f'{int(len(self.data) / self.num_examples * 100)}%')
            stdout.flush()

    def generate_example(self):
        sequence_values = [float(round(random.uniform(0, 1), self.number_of_decimal_places))
                           for i in range(self.sequence_length)]
        mask_indexes = [randrange(self.sequence_length), randrange(self.sequence_length)]
        mask_values = np.zeros(len(sequence_values))
        np.put(mask_values, mask_indexes[0], 1)
        np.put(mask_values, mask_indexes[1], 1)
        label = sum(sequence_values[index] for index in mask_indexes)
        return sequence_values, mask_values, label

    def write_data_to_json(self):
        print('\nWriting data to json file ....')
        file_name = f'sequence_length_{self.sequence_length}__num_examples_{self.num_examples}_' \
                    f'{self.mode}_{self.number_of_decimal_places}_dp.json'
        data = {
            'sequence_values': [example[0] for example in self.data],
            'sequence_masks': [np.ndarray.tolist(example[1]) for example in self.data],
            'sequence_labels': [example[2] for example in self.data]
        }
        pathlib.Path(_out_path).mkdir(exist_ok=True, parents=True)
        with open(_out_path + f'/{file_name}', 'w') as p:
            json.dump(data, p)


if __name__ == '__main__':
    _out_path = f'D:/MyData/ml_code/dl-keras/datasets'
    GenerateData(_out_path, sequence_length=600, num_examples=100000, number_of_decimal_places=1,
                 mode='train')
