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

settings_file = './settings-table-2.json'
logger.debug('settings file : %s' % settings_file)
with open(settings_file, 'r') as settings_fp:
    settings = json.load(settings_fp)

logger.debug('settings: %s' % settings)

headings = settings['headings']
input_folder = settings['input_folder']
input_file = settings['input_file']

full_file_name = input_folder + input_file
data = pd.read_csv(full_file_name, nrows=2)
actual_headings = data.columns.values
logger.debug('headings: %s' % actual_headings)

data = pd.read_csv(full_file_name, usecols=headings)
logger.debug('data has shape: %d x %d' % data.shape)
logger.debug(data.head(5))

logger.debug('done')
finish_time = time.time()
elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
logger.info('Time: {:0>2}:{:0>2}:{:05.2f}'.format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
console_handler.close()
logger.removeHandler(console_handler)
