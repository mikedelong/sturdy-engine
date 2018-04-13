import json
import logging
import time

import pandas as pd

start_time = time.time()
formatter = logging.Formatter('%(asctime)s : %(name)s :: %(levelname)s : %(message)s')
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
console_handler.setLevel(logging.DEBUG)
logger.debug('started')

settings_file = './settings-table-4.json'
logger.debug('settings file : %s' % settings_file)
with open(settings_file, 'r') as settings_fp:
    settings = json.load(settings_fp)

logger.debug('settings: %s' % settings)

codes = settings['codes']
file_infix = settings['file_infix']
file_prefix = settings['file_prefix']
file_suffixes = settings['file_suffixes']
file_suffix = settings['file_suffix']
input_folder = settings['input_folder']
join_column = settings['join_column']
rename_columns = settings['rename_columns']
usecols_0 = settings['usecols_0']
usecols_1 = settings['usecols_1']

for code in codes:
    file_names = [input_folder + file_prefix + str(code) + file_infix + file_type + file_suffix for file_type in
                  file_suffixes]
    logger.debug(file_names)

    frame_0 = pd.read_csv(file_names[0], usecols=usecols_0)
    frame_1 = pd.read_csv(file_names[1], usecols=usecols_1)
    frame_2 = pd.read_csv(file_names[2], usecols=usecols_1)
    frame_2.rename(columns=rename_columns, inplace=True)
    joined = frame_0.merge(frame_1, on=join_column)
    result = joined.merge(frame_2, on=join_column)

    logger.debug('result columns: %s' % result.columns.values)
    logger.debug('result has shape %d x %d' % result.shape)

logger.debug('done')
finish_time = time.time()
elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
logger.info('Time: {:0>2}:{:0>2}:{:05.2f}'.format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
console_handler.close()
logger.removeHandler(console_handler)
