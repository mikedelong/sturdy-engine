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

input_folder = '../processed/'
input_files = settings['input_files']
input_files = [item.replace('.txt', '.csv') for item in input_files]

counts = Counter()
file_count = 0
# todo move this to a setting
limit = 2000
most_common_count = settings['most_common_count']

for item in input_files:
    if file_count < limit:
        file_count += 1
        full_file_name = input_folder + item
        data = pd.read_csv(full_file_name, nrows=2)
        values = data.columns.values

        logger.debug('%s : %s' % (item, values))
        for value in values:
            counts[value] += 1

logger.debug('there are %d unique column headings ' % len(counts))
most_common = counts.most_common(min(most_common_count, len(counts)))
labels = [item[0] for item in most_common]
values = [item[1] for item in most_common]
sum_most_common = sum(values)
sum_all = sum(counts.values())
logger.debug(most_common)
logger.debug('all counts: %d in top : %d difference: %d' % (sum_all, sum_most_common, sum_all - sum_most_common))

indexes = np.arange(len(labels))
width = 0.8

plt.figure(figsize=(11, 8))
plt.bar(indexes, values, width)
plt.xticks(indexes + width * 0.5, labels, rotation=90)
plt.tight_layout()

output_folder = settings['vertical_bar_chart_output_folder']
output_file = settings['vertical_bar_chart_output_file']
full_output_file_name = output_folder + output_file
logger.debug('writing vertical bar chart to %s' % full_output_file_name)
plt.savefig(full_output_file_name)

plt.clf()
# todo make this contingent on the number of records in the most common
plt.figure(figsize=(8, 32))
values.reverse()
labels.reverse()
plt.barh(indexes, values, width)
plt.yticks(indexes + width * 0.5, labels)
plt.ylim(0, len(labels))

plt.grid(True)
plt.tight_layout()

output_folder = settings['horizontal_bar_chart_output_folder']
output_file = settings['horizontal_bar_chart_output_file']
full_output_file_name = output_folder + output_file
logger.debug('writing horizontal bar chart to %s' % full_output_file_name)
plt.savefig(full_output_file_name)

logger.debug('done')
finish_time = time.time()
elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
logger.info('Time: {:0>2}:{:0>2}:{:05.2f}'.format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
console_handler.close()
logger.removeHandler(console_handler)
