#!/usr/bin/env python
'''
reports
'''

__version__ = '0.0.1'

import logging
log = logging.getLogger(__name__)

def initialize_logging(level=logging.DEBUG):
    global log
    log.setLevel(level)

    ch = logging.StreamHandler()
    fh = logging.FileHandler('monthly_report.log')
    ch.setLevel(level)
    fh.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    log.addHandler(ch)
    log.addHandler(fh)


initialize_logging()

