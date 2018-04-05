import json
import logging
import time
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
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

input_folder = '../output/'
input_files = settings['input_files']
input_files = [item.replace('.txt', '.csv') for item in input_files]

counts = Counter()
file_count = 0
limit = 2000

for item in input_files:
    if file_count < limit:
        full_file_name = input_folder + item
        data = pd.read_csv(full_file_name, nrows=2)
        values = data.columns.values

        logger.debug('%s : %s' % (item, values))
        for item in values:
            counts[item] += 1

logger.debug('there are %d unique column headings ' % len(counts))
most = counts.most_common(40)
labels = [item[0] for item in most]
values = [item[1] for item in most]
logger.debug(most)

indexes = np.arange(len(labels))
width = 0.9

plt.figure(figsize=(11, 8))
plt.bar(indexes, values, width)
plt.xticks(indexes + width * 0.5, labels, rotation=90)
plt.tight_layout()

plt.show()

logger.debug('done')
finish_time = time.time()
elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
logger.info('Time: {:0>2}:{:0>2}:{:05.2f}'.format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
console_handler.close()
logger.removeHandler(console_handler)
