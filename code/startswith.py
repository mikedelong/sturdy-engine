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
settings_file = './settings-headings.json'
logger.debug('settings file : %s' % settings_file)
with open(settings_file, 'r') as settings_fp:
    settings = json.load(settings_fp)

logger.debug('settings: %s' % settings)

# todo move to a setting
input_folder = '../processed/'
input_files = settings['input_files']
input_files = [item.replace('.txt', '.csv') for item in input_files]

file_count = 0
limit = 2000

starts_with_string = settings['starts_with']
for item in input_files:
    if file_count < limit:
        file_count += 1
        full_file_name = input_folder + item
        data = pd.read_csv(full_file_name, nrows=2)
        headings = data.columns.values
        for heading in headings:
            if heading.startswith(starts_with_string):
                logger.debug('file %s has heading [%s]' % (item, heading))

logger.debug('done')
finish_time = time.time()
elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
logger.info('Time: {:0>2}:{:0>2}:{:05.2f}'.format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
console_handler.close()
logger.removeHandler(console_handler)
