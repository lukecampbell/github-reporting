from reports import log 
from dateutil.parser import parse as dateparse
from reports.config import REPOS

from reports.github import count_issues_created
from reports.github import count_issues_closed
from reports.github import count_pull_requests_opened
from reports.github import count_pull_requests_closed
from reports.github import count_comments_created
from reports.github import count_commits
from reports.github import count_releases

import argparse
import csv


def main(args):
    '''
    Generates statistics on all repositories
    '''
    start = dateparse(args.start_date)
    end = dateparse(args.end_date)
    log.info("Initializing %s", args.filename)
    with open(args.filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)

        csvwriter.writerow([
            'repo',
            'issues created',
            'issues closed',
            'pull requests opened',
            'pull requests closed',
            'comments created',
            'commits',
            'releases'])

        for repo in REPOS:
            log.info("Getting report statistics on %s", repo)
            stats = (
                repo,
                count_issues_created(repo, start, end),
                count_issues_closed(repo, start, end),
                count_pull_requests_opened(repo, start, end),
                count_pull_requests_closed(repo, start, end),
                count_comments_created(repo, start, end),
                count_commits(repo, start, end),
                count_releases(repo, start, end)
            )
            csvwriter.writerow([str(i) for i in stats])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate IOOS Monthly Report')
    parser.add_argument('filename', help='Start Date')
    parser.add_argument('start_date', help='Start Date')
    parser.add_argument('end_date', help='End Date')
    args = parser.parse_args()


    main(args)

