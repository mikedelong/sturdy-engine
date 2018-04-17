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

settings_file = './settings-table-6.json'
logger.debug('settings file : %s' % settings_file)
with open(settings_file, 'r') as settings_fp:
    settings = json.load(settings_fp)

logger.debug('settings: %s' % settings)

headings_of_interest = settings['headings_of_interest']
input_files = settings['input_files']
input_folder = settings['input_folder']
for input_file in input_files:
    full_input_file = input_folder + input_file
    logger.debug('input file : %s' % full_input_file)
    data = pd.read_csv(full_input_file, nrows=2)
    headings = data.columns.values
    logger.debug('headings: %s' % headings)
    data = pd.read_csv(full_input_file, usecols=headings_of_interest)
    logger.debug('data has shape %d x %d' % data.shape)
    logger.debug('data has counts: \n%s' % data.count())
    logger.debug('data head: \n%s' % data.head(20))

logger.debug('done')
finish_time = time.time()
elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
logger.info('Time: {:0>2}:{:0>2}:{:05.2f}'.format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
console_handler.close()
logger.removeHandler(console_handler)
