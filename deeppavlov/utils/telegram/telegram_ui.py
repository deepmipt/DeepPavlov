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
from typing import Union

from deeppavlov.core.common.file import read_json
from deeppavlov.core.common.paths import get_settings_path
from deeppavlov.utils.connector import TelegramBot
from deeppavlov.utils.server.server import SERVER_CONFIG_FILENAME

log = getLogger(__name__)


def interact_model_by_telegram(model_config: Union[str, Path, dict],
                               token=None):

    server_config_path = get_settings_path() / SERVER_CONFIG_FILENAME
    telegram_server_params = read_json(server_config_path)['telegram_defaults']
    telegram_server_params['token'] = token or telegram_server_params['token']

    if not telegram_server_params['token']:
        e = ValueError('Telegram token required: initiate -t param or telegram_defaults/token '
                       'in server configuration file')
        log.error(e)
        raise e

    bot = TelegramBot(model_config, telegram_server_params)
    bot.polling()
