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

# read the input filename from a JSON file
settings_file = './settings-table-3.json'
logger.debug('settings file : %s' % settings_file)
with open(settings_file, 'r') as settings_fp:
    settings = json.load(settings_fp)

logger.debug('settings: %s' % settings)

headings = settings['headings']
input_folder = settings['input_folder']

file_prefix = settings['file_prefix']
enterprise_location_codes = settings['enterprise_location_codes']
file_infix = settings['file_infix']
file_suffixes = settings['file_suffixes']
file_suffix = settings['file_suffix']
join_column = settings['join_column']
column_alias = settings['column_alias']
mapper = {column_alias[1]: column_alias[0]}

for elc in enterprise_location_codes:
    file_names = [input_folder + file_prefix + str(elc) + file_infix + file_type + file_suffix for file_type in
                  file_suffixes]
    logger.debug(file_names)
    frames = [pd.read_csv(item) for item in file_names]
    frames = [item.rename(columns=mapper) for item in frames]
    logger.debug('frames shapes: %s' % [item.shape for item in frames])

    t0 = frames[0].join(frames[1])

    logger.debug(t0.shape)
    # for file_name in input_files:
    #     full_file_name = input_folder + file_name
    #     data = pd.read_csv(full_file_name, nrows=2)
    #     actual_headings = data.columns.values
    #     logger.debug('headings: %s' % actual_headings)

    # if all([item in actual_headings for item in headings]):
    #     data = pd.read_csv(full_file_name, usecols=headings)
    #     logger.debug('data has shape: %d x %d' % data.shape)
    #     logger.debug(data.head(20))
    # else:
    #     logger.debug('missing headings are: %s' % set(headings).difference(set(actual_headings)))

logger.debug('done')
finish_time = time.time()
elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
logger.info('Time: {:0>2}:{:0>2}:{:05.2f}'.format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
console_handler.close()
logger.removeHandler(console_handler)
