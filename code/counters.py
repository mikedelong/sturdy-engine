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

# read the input filename from a JSON file
settings_file = './settings-headings.json'
logger.debug('settings file : %s' % settings_file)
with open(settings_file, 'r') as settings_fp:
    settings = json.load(settings_fp)

logger.debug('settings: %s' % settings)

# todo move this to a setting
input_folder = '../processed/'
input_files = settings['input_files']
input_files = [item.replace('.txt', '.csv') for item in input_files]
heading_of_interest = settings['heading_of_interest']

file_count = 0
limit = 2000
counts = Counter()

for item in input_files:
    if file_count < limit:
        file_count += 1
        full_file_name = input_folder + item
        data = pd.read_csv(full_file_name, nrows=2)
        headings = data.columns.values
        if heading_of_interest in headings:
            logger.debug(item)
            sub_data = pd.read_csv(full_file_name, usecols=[heading_of_interest])
            value_counts = sub_data[heading_of_interest].value_counts()
            for key in value_counts.index:
                value = value_counts[key]
                counts[key] += value

            logger.debug(counts)

# most_common_count = 1000
# most_common = counts.most_common(most_common_count)
# sum_most_common = sum([item[1] for item in most_common])
# sum_all = sum(counts.values())
# logger.debug(most_common)
# logger.debug('all counts: %d in top : %d difference: %d' % (sum_all, sum_most_common, sum_all - sum_most_common))
# logger.debug('most common %d accounts for %d%% of total' % (most_common_count, 100 * sum_most_common / sum_all))

logger.debug('done')
finish_time = time.time()
elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
logger.info('Time: {:0>2}:{:0>2}:{:05.2f}'.format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
console_handler.close()
logger.removeHandler(console_handler)
