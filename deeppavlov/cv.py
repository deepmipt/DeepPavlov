"""
Copyright 2017 Neural Networks and Deep Learning lab, MIPT

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import argparse
from pathlib import Path
import sys
import numpy as np
from itertools import product
import os

p = (Path(__file__) / ".." / "..").resolve()
sys.path.append(str(p))

from deeppavlov.core.common.file import read_json, save_json
from deeppavlov.core.common.log import get_logger
from deeppavlov.core.commands.train import train_evaluate_model_from_config, get_iterator_from_config, read_data_by_config
from sklearn.model_selection import KFold
from deeppavlov.core.commands.utils import expand_path

PARAM_RANGE_SUFFIX_NAME = '_range'
SAVE_PATH_ELEMENT_NAME = 'save_path'
BACKUP_SUFFIX_FILENAME = '_backuped'
log = get_logger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("config_path", help="path to a pipeline json config", type=str)
parser.add_argument("--folds", help="number of folds", type=str, default='5')
parser.add_argument("--search_type", help="search type: grid or random search", type=str, default='grid')


def find_config(pipeline_config_path: str):
    if not Path(pipeline_config_path).is_file():
        configs = [c for c in Path(__file__).parent.glob(f'configs/**/{pipeline_config_path}.json')
                   if str(c.with_suffix('')).endswith(pipeline_config_path)]  # a simple way to not allow * and ?
        if configs:
            log.info(f"Interpreting '{pipeline_config_path}' as '{configs[0]}'")
            pipeline_config_path = str(configs[0])
    return pipeline_config_path

def delete_saved_model(models_paths):
    for model_path in models_paths:
        path = expand_path(model_path)
        if os.path.isfile(path):
            os.remove(path)

def backup_saved_models(models_paths):
    for model_path in models_paths:
        path = expand_path(model_path)
        if os.path.isfile(path):
            os.rename(path, expand_path(model_path+BACKUP_SUFFIX_FILENAME))

def restore_saved_models(models_paths):
    for model_path in models_paths:
        path = expand_path(model_path)
        backuped_path = expand_path(model_path+BACKUP_SUFFIX_FILENAME)
        if os.path.isfile(backuped_path):
            os.rename(backuped_path, path)


def calc_loocv_score(config, data, models_paths, target_metric):

    all_data = data['train'] + data['valid']
    m = len(all_data)
    all_scores = []
    for i in range(m):
        data_i = {}
        data_i['train'] = all_data.copy()
        data_i['valid'] = [data_i['train'].pop(i)]
        data_i['test'] = []
        iterator = get_iterator_from_config(config, data_i)
        delete_saved_model(models_paths)
        score = train_evaluate_model_from_config(config, iterator=iterator)
        all_scores.append(score['valid'][target_metric])

    return np.mean(all_scores)

def calc_cvfolds_score(config, data, n_folds, models_paths, target_metric):

    all_data = data['train'] + data['valid']
    all_scores = []

    kf = KFold(n_splits=n_folds, shuffle=True)

    for train_index, valid_index in kf.split(all_data):
        data_i = {}
        data_i['train'] = [all_data[i] for i in train_index]
        data_i['valid'] = [all_data[i] for i in valid_index]
        data_i['test'] = []
        iterator = get_iterator_from_config(config, data_i)
        delete_saved_model(models_paths)
        score = train_evaluate_model_from_config(config, iterator=iterator)
        all_scores.append(score['valid'][target_metric])

    return np.mean(all_scores)


def get_best_params(combinations, scores, param_names, target_metric):
    max_id = np.argmax(scores)
    best_params = dict(zip(param_names, combinations[max_id]))
    best_params[target_metric] = scores[max_id]

    return best_params

def main():
    args = parser.parse_args()

    # read config
    pipeline_config_path = find_config(args.config_path)
    config_init = read_json(pipeline_config_path)
    config = config_init.copy()
    config_best_model = config_init.copy()
    data = read_data_by_config(config)
    # get target metric as first element in "train->metrics"
    target_metric = config_init['train']['metrics'][0]

    # prepare params search
    param_values = {}
    chainer_items = []
    models_paths = []
    for i, elem in enumerate(config['chainer']['pipe']):
        for key in elem.keys():
            # find params ranges in config
            if key.endswith(PARAM_RANGE_SUFFIX_NAME):
                param_values[key.partition(PARAM_RANGE_SUFFIX_NAME)[0]] = elem[key]
                chainer_items.append(i)
        if (('in_y' in elem) | ('fit_on' in elem) | ('fit_on_batch' in elem)) & (SAVE_PATH_ELEMENT_NAME in elem):
            models_paths.append(elem[SAVE_PATH_ELEMENT_NAME])

    # backup initial model files
    backup_saved_models(models_paths)

    # get cv scores
    if args.search_type == 'grid':
        # generate params combnations for grid search
        combinations = list(product(*param_values.values()))
        param_names = [k for k in param_values.keys()]

        # calculate cv scores
        scores=[]
        for comb in combinations:
            for i, param_value in enumerate(comb):
                config['chainer']['pipe'][chainer_items[i]][param_names[i]] = param_value

            if args.folds == 'loo':
                scores.append(calc_loocv_score(config, data, models_paths, target_metric))
            elif args.folds.isdigit():
                n_folds = int(args.folds)
                scores.append(calc_cvfolds_score(config, data, n_folds, models_paths, target_metric))
            else:
                raise NotImplementedError('Not implemented this type of CV')

        # get model with best score
        best_params_dict = get_best_params(combinations, scores, param_names, target_metric)
        log.info('Best model params: {}'.format(best_params_dict))
    else:
        raise NotImplementedError('Not implemented this type of search')

    # restore initial model files
    delete_saved_model(models_paths)
    restore_saved_models(models_paths)

    # save config
    for i, param_name in enumerate(best_params_dict.keys()):
        if param_name != target_metric:
            config_best_model['chainer']['pipe'][chainer_items[i]][param_name] = best_params_dict[param_name]
            config_best_model['chainer']['pipe'][chainer_items[i]].pop(param_name+PARAM_RANGE_SUFFIX_NAME)
    best_model_filename = pipeline_config_path.replace('.json', '_cvbest.json')
    save_json(config_best_model, best_model_filename)
    log.info('Best model saved in json-file: {}'.format(best_model_filename))


# try to run:
# --config_path path_to_config.json --folds 2
if __name__ == "__main__":
    main()

