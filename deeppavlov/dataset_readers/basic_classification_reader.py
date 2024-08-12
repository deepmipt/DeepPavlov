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



from logging import getLogger
from pathlib import Path
from collections import defaultdict

import pandas as pd
from tqdm import tqdm

from deeppavlov.core.common.registry import register
from deeppavlov.core.data.dataset_reader import DatasetReader
from deeppavlov.core.data.utils import download

log = getLogger(__name__)


@register('basic_classification_reader')
class BasicClassificationDatasetReader(DatasetReader):
    """
    Class provides reading dataset in .csv format
    """

    @overrides
    def read(self, data_path: str, url: str = None,
             format: str = "csv", class_sep: str = None,
             label_type: str = "str", *args, **kwargs) -> dict:
        """
        Read dataset from data_path directory.
        Reading files are all data_types + extension
        (i.e for data_types=["train", "valid"] files "train.csv" and "valid.csv" form
        data_path will be read)
        Args:
            data_path: directory with files
            url: download data files if data_path not exists or empty
            format: extension of files. Set of Values: ``"csv", "json"``
            class_sep: string separator of labels in column with labels
            sep (str): delimeter for ``"csv"`` files. Default: None -> only one class per sample
            header (int): row number to use as the column names
            names (array): list of column names to use
            orient (str): indication of expected JSON string format
            lines (boolean): read the file as a json object per line. Default: ``False``
            label_type(str): expected type of labels. Default: ``"str"``
        Returns:
            dictionary with types from data_types.
            Each field of dictionary is a list of tuples (x_i, y_i)
        """
        def row_list_process(row, y):
            if pd.isna(row[y]):
                return []
            else:
                return [label_type(label) for label in str(row[y]).split(class_sep)]

        data_types = ["train", "valid", "test"]

        train_file = kwargs.get('train', 'train.csv')

        if not Path(data_path, train_file).exists():
            if url is None:
                raise Exception(
                    "data path {} does not exist or is empty, and download url parameter not specified!".format(
                        data_path))
            log.info("Loading train data from {} to {}".format(url, data_path))
            download(source_url=url, dest_file_path=Path(data_path, train_file))

        data = {"train": [],
                "valid": [],
                "test": []}

        supported_label_types = ['int','str','float']
        error_msg = f'Wrong label type {label_type} given! Needs to be one of the built-in Python types'
        if label_type not in supported_label_types:
            raise Exception(error_msg)
        label_type = eval(label_type)
        data=defaultdict(list)
        for data_type in data_types:
            file_name = kwargs.get(data_type, '{}.{}'.format(data_type, format))
            if file_name is None:
                continue

            file = Path(data_path).joinpath(file_name)
            if file.exists():
                if format == 'csv':
                    keys = ('sep', 'header', 'names')
                    options = {k: kwargs[k] for k in keys if k in kwargs}
                    print(file)
                    df = pd.read_csv(file, **options)
                elif format == 'json':
                    keys = ('orient', 'lines')
                    options = {k: kwargs[k] for k in keys if k in kwargs}
                    df = pd.read_json(file, **options)
                else:
                    raise Exception('Unsupported file format: {}'.format(format))

                x = kwargs.get("x", "text")
                y = kwargs.get('y', 'labels')

                for _, row in tqdm(df.iterrows()):
                    try:
                        if isinstance(x, list):
                            x_text = [row[x_] for x_ in x]
                        else:
                            x_text = row[x]
                        if class_sep is None:
                            y_label = label_type(row[y])
                        else:
                            y_label = row_list_process(row, y)
                        data[data_type].append((x_text, y_label))
                    except Exception as e:
                        print(f'Error processing {row}: {e}')
                        raise e
            else:
                log.warning("Cannot find {} file".format(file))

        return data
