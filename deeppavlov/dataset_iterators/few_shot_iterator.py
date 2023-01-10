# Copyright 2017 Neural Networks and Deep Learning lab, MIPT
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import json
from logging import getLogger
from pathlib import Path
from random import Random
from typing import Dict, Any, List, Tuple, Optional
from collections import defaultdict

from deeppavlov.core.common.registry import register
from deeppavlov.core.data.data_learning_iterator import DataLearningIterator

ENTAILMENT = 'entailment'
NON_ENTAILMENT = 'non_entailment'

SUPPORT_DATASET_PATH="~/.deeppavlov/preprocessed_datasets/support_dataset.json"

log = getLogger(__name__)


@register('few_shot_iterator')
class FewShotIterator(DataLearningIterator):
    """
    Class gets data dictionary from DatasetReader instance, samples N examples from each class of the training data
    and, if necessary, returns data in the NLI format (all possible pairs of training sentences).

    Args:
        data: dictionary of data with fields "train", "valid" and "test" (or some of them)
        seed: random seed for iterating
        shuffle: whether to returned shuffled examples
        shot: number of examples to sample for each class in training data
        shot_test: number of examples to sample for each class in validation and test
        return_nli_format: whether to return the data in NLI format - pairs of sentences separated by a special token

    Attributes:
        data: dictionary of data with fields "train", "valid" and "test" (or some of them)
        """

    def __init__(self,
                 data: Dict[str, List[Tuple[Any, Any]]],
                 seed: int = None,
                 shuffle: bool = True,
                 shot: Optional[int] = None,
                 shot_test: Optional[int] = None,
                 return_nli_format: bool = False
                 ) -> None:
        self.shot = shot
        self.shot_test = shot_test
        self.shuffle = shuffle
        self.random = Random(seed)

        self.train = self.delete_oos(data.get('train', []))
        self.valid = self.delete_oos(data.get('valid', []))
        self.test = self.delete_oos(data.get('test', []))

        self.train = self.get_shot_examples(self.train, self.shot)
        self.valid = self.get_shot_examples(self.valid, self.shot_test)
        self.test = self.get_shot_examples(self.test, self.shot_test)

        save_path = Path(SUPPORT_DATASET_PATH).expanduser()
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with save_path.open("w") as file:
            json_dict = {"columns": ["text", "category"]}
            json_dict["data"] = [[text, label] for text, label in self.train]
            json.dump(json_dict, file, indent=4)

        if return_nli_format:
            self.train = self.convert2nli(self.train)
            self.valid = self.convert2nli(self.valid)
            self.test = self.convert2nli(self.test)

        self.data = {
            'train': self.train,
            'valid': self.valid,
            'test': self.test,
            'all': self.train + self.test + self.valid
            }
    
    def _gather_info(self, data: List[Tuple[Any, Any]]) -> Tuple[Dict, Dict]:
        unique_labels = set([label for text, label in data])

        label2examples = defaultdict(list)
        for text, label in data:
            label2examples[label].append(text)

        label2negative = {label: unique_labels - {label} for label in unique_labels}

        return label2examples, label2negative

    def convert2nli(self, data: List[Tuple[Any, Any]]) -> List[Tuple[Tuple[Any, Any], Any]]:
        if len(data) == 0:
            return data

        label2examples, label2negative = self._gather_info(data)
        nli_triplets = []

        # negative examples
        for text, label in data:
            for negative_label in label2negative[label]:
                for negative_example in label2examples[negative_label]:
                    nli_triplets.append([[text, negative_example], NON_ENTAILMENT])

        # positive examples
        for text, label in data:
            for positive_example in label2examples[label]:
                if positive_example != text:
                    nli_triplets.append([[text, positive_example], ENTAILMENT])
        
        if self.shuffle:
            self.random.shuffle(nli_triplets)

        return nli_triplets
        
    def delete_oos(self, data: List[Tuple[Any, Any]]) -> List[Tuple[Any, Any]]:
        filtered_data = []
        for text, label in data:
            if label != 'oos':
                filtered_data.append([text, label])
        return filtered_data

    def get_shot_examples(self, data: List[Tuple[Any, Any]], shot: int) -> List[Tuple[Any, Any]]:
        if shot is None:
            return data

        # shuffle data to select shot-examples
        self.random.shuffle(data)

        data_dict = defaultdict(list)
        for text, label in data:
            if len(data_dict[label]) < shot:
                data_dict[label].append(text)
        
        if min(len(x) for x in data_dict.values()) < shot:
            log.warning(f"Some labels have less than {shot} examples")

        new_data = []
        for label in data_dict.keys():
            for text in data_dict[label]:
                new_data.append((text, label))

        if self.shuffle:
            self.random.shuffle(new_data)

        return new_data
