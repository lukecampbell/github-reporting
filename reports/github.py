#!/usr/bin/env python
'''
monthly_report.py

A utility script to generate statistics about the github activity for certain
repositories
'''

from requests.auth import HTTPBasicAuth
from reports.config import ACCESS_TOKEN, REPOS
from dateutil.parser import parse as dateparse

import requests
import pytz
import csv
import re
import argparse
import logging

logger = logging.getLogger(__name__)

class APIError(IOError):
    '''
    Exception for API requests that aren't successful
    '''
    response = None

    def __init__(self, message, response):
        self.response = response
        IOError.__init__(self, message)

def set_tz(dt):
    '''
    Sets a timezone to a potentially naive datetime
    '''
    if dt is None:
        return None
    if dt.tzinfo is not None:
        return dt
    return pytz.utc.localize(dt)



def comments(repo, start, end=None):
    '''
    Fetches the comments on issues
    '''
    start = set_tz(start)
    end   = set_tz(end)
    base_url = u'https://api.github.com/repos/'
    url = base_url + repo + '/issues/comments?since=' + start.isoformat()
    comments_response = github_api_get(url)
    return comments_response

def commits(repo, start, end):
    '''
    Fetches the commits
    '''
    start = set_tz(start)
    end   = set_tz(end)
    base_url = u'https://api.github.com/repos/'
    url = base_url + repo + '/commits?since=' + start.isoformat() + '&until=' + end.isoformat()
    commits_response = github_api_get(url)
    return commits_response


def issues(repo, start, end=None):
    '''
    Fetches the issues
    '''
    start = set_tz(start)
    end   = set_tz(end)
    base_url = u'https://api.github.com/repos/'
    url = base_url + repo + '/issues?state=all&since=' + start.isoformat()
    issues_response = github_api_get(url)
    return issues_response

def releases(repo, start, end):
    '''
    Fetches the releases
    '''
    start = set_tz(start)
    end   = set_tz(end)
    base_url = u'https://api.github.com/repos/'
    url = base_url + repo + '/releases?since=' + start.isoformat() + '&until=' + end.isoformat()
    releases_response = github_api_get(url)
    retval = []
    for release_doc in releases_response:
        doc_start = dateparse(release_doc['created_at'])
        if start <= doc_start and doc_start <= end:
            retval.append(release_doc)

    return retval

def comments_created(repo, start, end=None):
    '''
    Generates statistics on comments created
    '''
    start = set_tz(start)
    end   = set_tz(end)
    comments_response = comments(repo, start, end)
    def comment_filter(record):
        dt = dateparse(record['created_at'])
        if end:
            return dt > start and dt < end 
        return dt > start
    comments_response = filter(comment_filter, comments_response)
    return comments_response


def issues_created(repo, start, end=None):
    '''
    Generates statistics on issues created
    '''
    start = set_tz(start)
    end   = set_tz(end)
    issues_response = issues(repo, start, end)
    def issue_filter(record):
        dt = dateparse(record['created_at'])
        if 'pull_request' in record:
            return False
        if end:
            return dt > start and dt < end 
        return dt > start
    issues_response = filter(issue_filter, issues_response)
    return issues_response

def issues_closed(repo, start, end=None):
    '''
    Generates statistics on issues closed
    '''
    start = set_tz(start)
    end   = set_tz(end)
    issues_response = issues(repo, start, end)
    def issue_filter(record):
        if not record['closed_at']:
            return False
        dt = dateparse(record['closed_at'])
        if 'pull_request' in record:
            return False
        if end:
            return dt > start and dt < end 
        return dt > start
    issues_response = filter(issue_filter, issues_response)
    return issues_response

def pull_requests_opened(repo, start, end=None):
    '''
    Generates statistics on pull-requests opened
    '''
    start = set_tz(start)
    end   = set_tz(end)
    issues_response = issues(repo, start, end)
    def issue_filter(record):
        dt = dateparse(record['created_at'])
        if 'pull_request' not in record:
            return False
        if end:
            return dt > start and dt < end 
        return dt > start
    issues_response = filter(issue_filter, issues_response)
    return issues_response

def pull_requests_closed(repo, start, end=None):
    '''
    Generates statistics on pull-requests closed
    '''
    start = set_tz(start)
    end   = set_tz(end)
    issues_response = issues(repo, start, end)
    def issue_filter(record):
        if not record['closed_at']:
            return False
        dt = dateparse(record['closed_at'])
        if 'pull_request' not in record:
            return False
        if end:
            return dt > start and dt < end 
        return dt > start
    issues_response = filter(issue_filter, issues_response)
    return issues_response

def count_comments_created(repo, start, end=None):
    '''
    Counts the number of comments created between start and end datetimes
    '''
    return len(comments_created(repo, start, end))

def count_commits(repo, start, end):
    '''
    Counts the number of commits created between start and end datetimes
    '''
    return len(commits(repo, start, end))

def count_issues_created(repo, start, end=None):
    '''
    Counts the number of issues created between start and end datetimes
    '''
    return len(issues_created(repo, start, end))

def count_issues_closed(repo, start, end=None):
    '''
    Counts the number of issues closed between start and end datetimes
    '''
    return len(issues_closed(repo, start, end))

def count_pull_requests_opened(repo, start, end=None):
    '''
    Counts the number of pull-requests opened between start and end datetimes
    '''
    return len(pull_requests_opened(repo, start, end))

def count_pull_requests_closed(repo, start, end=None):
    '''
    Counts the number of pull-requests closed between start and end datetimes
    '''
    return len(pull_requests_closed(repo, start, end))

def count_releases(repo, start, end):
    '''
    Counts the number of releases created between start and end datetimes
    '''
    return len(releases(repo, start, end))


def github_api_get(url, follow_next=True):
    '''
    Performs a github-api aware GET request
    '''
    # Perform the request
    response = requests.get(url, auth=HTTPBasicAuth(ACCESS_TOKEN, ''))

    if response.status_code != 200:
        logger.error("HTTP %s: %s", response.status_code, response.text)
        raise APIError("(%s) HTTP Code %s" % (url,response.status_code), response)

    # Wait time to parse out the links
    links = parse_links(response)
    issues_dict = response.json()
    if follow_next and 'next' in links:
        next_page = github_api_get(links['next'])
        if isinstance(issues_dict, list):
            return issues_dict + next_page
        else:
            issues_dict.update(next_page)
            return issues_dict
    return issues_dict

def parse_links(response):
    '''
    The HTTP response in the github API will use pagification and present the
    follow-up links in the headers. This function parses those out.
    '''
    pages = response.headers.get('link', '')
    pages = pages.split(',')
    links = {}
    for page in pages:
        regex_links(page, links)
    return links

def regex_links(link_response, links):
    '''
    Parses out the type and URL of the links provided by the github API
    pagification
    '''
    matches = re.search(r' ?<(.*)>; rel="(next|last)"', link_response)
    if matches:
        page_name = matches.groups()[1]
        page_url = matches.groups()[0]
        links[page_name] = page_url


    
