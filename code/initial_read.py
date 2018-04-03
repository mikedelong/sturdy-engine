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
settings_file = './settings.json'
logger.debug('settings file : %s' % settings_file)
with open(settings_file, 'r') as settings_fp:
    settings = json.load(settings_fp)

logger.debug('settings: %s' % settings)

for setting in ['input_folder', 'input_files']:
    if setting not in settings.keys():
        logger.warning('essential setting %s not found. Quitting.')
        quit()

input_folder = settings['input_folder']
input_folder = input_folder + '/' if not input_folder.endswith('/') else input_folder
input_files = settings['input_files']

for input_file in input_files:
    full_input_file = input_folder + input_file
    logger.debug('reading data from input file %s' % full_input_file)

    with open(full_input_file, 'r') as input_csv_fp:
        line_count = 0
        names = list()
        for row in input_csv_fp:
            if row.startswith('>DESCRIPTION'):
                line_count += 1
                pass
            elif row.startswith('>END'):
                logger.debug('file: %s, skip to %d' % (full_input_file, line_count))
                break
            else:
                line_count += 1
                tokens = row.split('.')
                names.append(tokens[-1].strip())

    data = pd.read_csv(full_input_file, skiprows=line_count + 1, sep='|', header=None, names=names,
                       skipinitialspace=True, skip_blank_lines=True, parse_dates=True)
    logger.info('data frame from %s has shape %d x %d' % (full_input_file, data.shape[0], data.shape[1]))
    logger.debug('data frame has columns %s' % data.columns.values)
    for column in data.columns.values:
        if 'XXXX' in column:
            # counts = data[column].value_counts()
            unique_values = data[column].unique()
            unique_values = [item.strip() if type(item) == str else item for item in unique_values]
            logger.debug('column %s has unique values %s' % (column, unique_values))
            # counts.hist()
            # plt.show()
    # write the clean data to a file
    output_file = input_file.replace('.txt', '.csv')
    output_folder = '../output/'
    full_output_file = output_folder + output_file
    logger.debug('writing clean data to %s' % full_output_file)
    data.to_csv(full_output_file, index=False)

logger.debug('done')
finish_time = time.time()
elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
logger.info("Time: {:0>2}:{:0>2}:{:05.2f}".format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
