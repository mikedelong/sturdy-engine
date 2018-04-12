import json
import logging
import time
from collections import Counter

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

settings_file = './settings-table-1.json'
logger.debug('settings file : %s' % settings_file)
with open(settings_file, 'r') as settings_fp:
    settings = json.load(settings_fp)

logger.debug('settings: %s' % settings)

input_folder = settings['input_folder']
input_files = settings['input_files']
input_files = [item.replace('.txt', '.csv') for item in input_files]
headings_of_interest = settings['headings_of_interest']

file_count = 0
counts = Counter()
files_counted = 0
augmented_counted = 0

for item in input_files:
    file_count += 1
    full_file_name = input_folder + item
    data = pd.read_csv(full_file_name, nrows=2)
    headings = data.columns.values

    if all([heading in headings for heading in headings_of_interest]):
        sub_data = pd.read_csv(full_file_name, usecols=headings_of_interest)
        logger.debug('file %s has data of interest that is %s and the other columns are %s' %
                     (item, sub_data.shape,
                      list(set(data.columns.values).difference(set(headings_of_interest)))))
        this_heading = headings_of_interest[0]
        interesting = sub_data[sub_data[this_heading].isin(['T', 'U'])]
        logger.debug('interesting record count : %d x %d' % interesting.shape)
        if interesting.shape[0] > 0:
            logger.debug(interesting.head(5))
        files_counted += 1

logger.debug('we found %d files of interest' % files_counted)


logger.debug('done')
finish_time = time.time()
elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
logger.info('Time: {:0>2}:{:0>2}:{:05.2f}'.format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
console_handler.close()
logger.removeHandler(console_handler)
