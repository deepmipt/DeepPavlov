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

import random
from pathlib import Path
from typing import Dict, List, Tuple
import xml.etree.ElementTree as ET

from deeppavlov.core.data.dataset_reader import DatasetReader
from deeppavlov.core.common.registry import register
from deeppavlov.core.commands.utils import expand_path


@register('paraphraser_reader')
class ParaphraserReader(DatasetReader):
    """The class to read the paraphraser.ru dataset from files.

    Please, see https://paraphraser.ru.

    Args:
        data_path: A path to a folder with dataset files.
        num_samples: A number of data samples to use in ``train``, ``validation`` and ``test`` mode.
        seed: Random seed.
    """

    def read(self,
             data_path: str,
             num_samples: int = None,
             seed: int = None, *args, **kwargs) -> Dict[str, List[Tuple[List[str], int]]]:
        random.seed(seed)
        data_path = expand_path(data_path)
        train_fname = Path(data_path) / 'paraphrases.xml'
        test_fname =  Path(data_path) / 'paraphrases_gold.xml'
        data = self.build_data(train_fname)
        random.shuffle(data)
        train_data = data[:-1000][:num_samples]
        valid_data = data[-1000:][:num_samples]
        test_data = self.build_data(test_fname)[:num_samples]
        dataset = {"train": train_data, "valid": valid_data, "test": test_data}
        return dataset

    def build_data(self, fname):
        with open(fname, 'r') as labels_file:
            context = ET.iterparse(labels_file, events=("start", "end"))
            # turn it into an iterator
            context = iter(context)
            # get the root element
            event, root = next(context)
            same_set = set()
            questions = []
            labels = []
            for event, elem in context:
                if event == "end" and elem.tag == "paraphrase":
                    question = []
                    y = None
                    for child in elem.iter():
                        if child.get('name') == 'text_1':
                            question.append(child.text.lower())
                        if child.get('name') == 'text_2':
                            question.append(child.text.lower())
                        if child.get('name') == 'class':
                            y = 1 if int(child.text) >= 0 else 0
                    root.clear()
                    check_string = "\n".join(question)
                    if check_string not in same_set:
                        same_set.add(check_string)
                        questions.append(question)
                        labels.append(y)
            return list(zip(questions, labels))
