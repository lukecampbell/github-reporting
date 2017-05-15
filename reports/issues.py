#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
reports/issues.py
'''
from reports.github import issues
from reports.unicode_csv import UnicodeWriter
from reports import log
from dateutil.parser import parse as dateparse

import argparse


def main(args):
    '''
    Generates a CSV for the issues for a specific repo
    '''
    log.info('Initializing %s', args.filename)
    start = dateparse(args.start_date)
    end = dateparse(args.end_date)
    log.info('Getting issues from github %s', args.repository)
    response = issues(args.repository, start, end)
    rows = [(str(r['number']), r['title'], r['state'], str(r['closed_at'])) for r in response]
    with open(args.filename, 'wb') as csvfile:
        writer = UnicodeWriter(csvfile)
        writer.writerow(('Issue Number', 'Title', 'Status', 'Closed At'))
        writer.writerows(rows)
    log.info('Done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('repository', help='The github Repository in the form of owner/repo')
    parser.add_argument('filename', help='Start Date')
    parser.add_argument('start_date', help='Start Date')
    parser.add_argument('end_date', help='End Date')
    args = parser.parse_args()

    main(args)
