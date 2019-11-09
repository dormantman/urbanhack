import logging
import math
import os
import sys

import datetime


def init(filename: str = 'dmlogging.log', level: str = 'NOTSET', func_name: bool = False):
    print('Dm Logging Init')

    path = os.path.join('.dm', filename)
    date = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    func_name = ' %(funcName)s' if func_name else ''

    if not os.access('.dm', os.F_OK):
        os.mkdir('.dm')

    if not os.access(path, os.F_OK):
        with open(path, 'w', encoding='utf-8') as file:
            parent_frame = sys._getframe(1)
            parent_file = parent_frame.f_code.co_filename
            data = [
                '',
                '-------------------',
                '| Dm Logging Config |',
                '-------------------',
                '', '',
                'Config Info', '',
                'Created: {}'.format(date),
                'File name: {}'.format(filename),
                'The parent file: {}'.format(parent_file),
                'Init line: {}'.format('{}:{}'.format(parent_file, parent_frame.f_lineno)),
                'Size parent: {}'.format(__human_size__(os.stat(parent_file).st_size)),
            ]

            w_tab = 80
            for i in range(len(data)):
                data[i] = data[i].center(w_tab)
            data.append('\n')
            file.write('\n'.join(data))
    else:
        with open(path, 'a', encoding='utf-8') as file:
            data = '-- New session [{}] --'.format(date).center(80)
            file.write('\n{}\n'.format(data))

    """
               Levels 
         -----------------
        | CRITICAL  :  50 |
        | ERROR     :  40 |
        | WARNING   :  30 |
        | INFO      :  20 |
        | DEBUG     :  10 |
        | NOTSET    :   0 |
         -----------------
    """

    """
                       -----------------
                      | The keys to use |
                       -----------------
        Name              Description              Example

        name            - Short file name        | (example: 'function')
        msg, message    - Message text           |
        levelname       - Name of your level     | (example: 'INFO')
        levelno         - Int of your level      | (example: 20)
        pathname        - Full path to file      | (example: 'C:\\python\\...\\function.py')
        filename        - File name              | (example: 'function.py')
        exc_info        - Exception info         |
        exc_text        - Exception text         |
        stack_info      - Stack info             |
        lineno          - Line number            | (example: 39)
        funcName        - Function name          | (example: sqrt)
        created         - Creation time          | (example: 15005.0412)
        msecs           - Milli seconds          | (example: 67.6639)
        relativeCreated - Creation relative time | (example: 488.692045211792)
        thread          - Number thread          | (example: 10780)
        threadName      - Thread name            | (example: 'MainThread')
        process         - Number process         | (example: 14360)
        processName     - Process name           | (example: 'MainProcess')
        asctime         - Date format            | (example: '1917.09.01 13:09:52')

    """

    logging.basicConfig(
        format='%(pathname)s:%(lineno)d #%(levelname)s [%(asctime)s]{}: %(message)s'.format(func_name),
        level=['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'].index(level) * 10,
        handlers=[
            logging.FileHandler(path, encoding='utf-8'),
            logging.StreamHandler()
        ],
        datefmt='%Y.%m.%d %H:%M:%S'
    )


def __human_size__(bytes_size):
    units = ['bytes', 'KB', 'MB', 'GB', 'TB']
    order = int(math.log2(bytes_size) / 10) if bytes_size else 0
    return '{:.4g} {}'.format(bytes_size / (1 << (order * 10)), units[order])


if __name__ == '__main__':
    print('You must use function [ init ]')
    help(init)