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
from random import Random
from typing import Dict, Any, List, Tuple, Optional
from logging import getLogger
from pathlib import Path

import numpy as np
from overrides import overrides

from deeppavlov.core.common.registry import register
from deeppavlov.core.data.data_learning_iterator import DataLearningIterator

ENTAILMENT = 'entailment'
NON_ENTAILMENT = 'non_entailment'

log = getLogger(__name__)

@register('few_shot_iterator')
class FewShotIterator(DataLearningIterator):

    def __init__(self,
                 data: Dict[str, List[Tuple[Any, Any]]],
                 seed: int = None, 
                 shuffle: bool = True, 
                 shot: Optional[int] = None,
                 shot_test: Optional[int] = None,
                 save_path: Optional[str] = None,
                 return_nli_format: bool = False,
                 *args, **kwargs) -> None:
        self.shot = shot
        self.shot_test = shot_test
        self.shuffle = shuffle
        self.random = Random(seed)

        self.train = self.get_shot_examples(data.get('train', []), self.shot)
        self.valid = self.get_shot_examples(data.get('valid', []), self.shot_test)
        self.test = self.get_shot_examples(data.get('test', []), self.shot_test)

        if save_path is not None:
            save_path = Path(save_path).expanduser()
            save_path.parent.mkdir(parents=True, exist_ok=True)
            with save_path.open("w") as file:
                json_dict = {"columns": ["text","category"]}
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

    
    def _gather_info(self, data: List[Tuple[Any, Any]]):
        unique_labels = list(set([label for text, label in data]))

        label2examples = {}
        for label in unique_labels:
            label2examples[label] = []
        for text, label in data:
            label2examples[label].append(text)
        
        label2negative = {}
        for i, label in enumerate(unique_labels):
            label2negative[label] = unique_labels.copy()
            del label2negative[label][i]
        
        return label2examples, label2negative


    def convert2nli(self, data: List[Tuple[Any, Any]]) -> List[Tuple[Any, Any]]:
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
        

    def get_shot_examples(self, data, shot):
        if shot is None:
            return data
        
        # shuffle data to select shot-examples
        if self.shuffle:
            self.random.shuffle(data)

        data_dict = {}
        for _, label in data:
            data_dict[label] = []

        for text, label in data:
            if len(data_dict[label]) < shot:
                data_dict[label].append(text)
        
        if max(len(x) for x in data_dict.values()) < shot:
            log.warning(f"Some labels have less than \"shot\"={shot} examples")

        new_data = []
        for label in data_dict.keys():
            for text in data_dict[label]:
                new_data.append((text, label))
        return new_data
