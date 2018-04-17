from deeppavlov.core.data.dataset_reader import DatasetReader
from pathlib import Path
from deeppavlov.core.common.registry import register
from deeppavlov.core.data.utils import download_decompress, mark_done, is_done
from deeppavlov.core.commands.utils import expand_path
import pickle
import numpy as np


@register('ubuntu_reader')
class UbuntuReader(DatasetReader):

    def read(self, data_path):
        data_path = expand_path(data_path)
        self.download_data(data_path)
        fname = Path(data_path) / 'dataset_1MM/dataset.pkl'
        dataset = self.preprocess_data(fname)
        return dataset

    def download_data(self, data_path):
        if not is_done(Path(data_path)):
            download_decompress(url="http://lnsigo.mipt.ru/export/datasets/ubuntu_blobs.tgz",
                                download_path=data_path)
            mark_done(data_path)

    def preprocess_data(self, fname):

        with open(fname, 'rb') as f:
            data = pickle.load(f)
        a = list(zip(data[0]['c'], data[0]['r'], data[0]['y']))
        a = list(filter(lambda x: len(x[1]) != 0, a))
        data[0]['c'], data[0]['r'], data[0]['y'] = zip(*a)
        data[0]['r'] = list(data[0]['r'])
        all_resps = data[0]['r'] + data[1]['r'] + data[2]['r']
        all_resps = sorted(set([' '.join(map(str, el)) for el in all_resps]))
        vocab = {el[1]: el[0] for el in enumerate(all_resps)}
        train_resps = [vocab[' '.join(map(str, el))] for el in data[0]['r']]
        train_data = [[el[0], el[1]] for el in zip(data[0]['c'], train_resps, data[0]['y']) if el[2] == '1']
        train_data = [{"context": el[0], "response": el[1],
                       "pos_pool": [el[1]], "neg_pool": None}
                      for el in train_data]
        contexts = []
        val_resps = [vocab[' '.join(map(str, el))] for el in data[1]['r']]
        pos_resps = []
        neg_resps = []
        neg_resp = []
        for el in zip(data[1]['c'], val_resps, data[1]['y']):
            if el[2] == '1':
                contexts.append(el[0])
                pos_resps.append(el[1])
                if len(neg_resp) > 0:
                    neg_resps.append(neg_resp)
                    neg_resp = []
            else:
                neg_resp.append(el[1])
        prob = np.ones(len(vocab))
        prob[pos_resps[-1]] = 0
        prob /= np.sum(prob)
        neg_resp += list(np.random.choice(np.arange(len(vocab)), size=4, p=prob))
        neg_resps.append(neg_resp)
        val_data = list(zip(contexts, pos_resps, neg_resps))
        val_data = [{"context": el[0], "response": el[1],
                     "pos_pool": [el[1]], "neg_pool": el[2]} for el in val_data]

        contexts = []
        test_resps = [vocab[' '.join(map(str, el))] for el in data[2]['r']]
        pos_resps = []
        neg_resps = []
        neg_resp = []
        for el in zip(data[2]['c'], test_resps, data[2]['y']):
            if el[2] == '1':
                contexts.append(el[0])
                pos_resps.append(el[1])
                if len(neg_resp) > 0:
                    neg_resps.append(neg_resp)
                    neg_resp = []
            else:
                neg_resp.append(el[1])
        neg_resps.append(neg_resp)
        test_data = list(zip(contexts, pos_resps, neg_resps))
        test_data = [{"context": el[0], "response": el[1],
                     "pos_pool": [el[1]], "neg_pool": el[2]} for el in test_data]

        return {'train': train_data, 'valid': val_data, 'test': test_data}
