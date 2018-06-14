#!/usr/bin/env python

"""
ghstars.py
----------

Python 3.3+ script to sort repos by star count.
Zero-star repos are omitted.

Usage
.....

    python ghstars.py owner [owner2 owner3 ...]


Notes
.....

This script uses GH Public API, which has a rate limit.
You can easily exceed it if a big organization (ie,
Microsoft) is queried a couple times.
"""

import sys
import requests
from itertools import chain
from operator import itemgetter
from datetime import datetime

__version__ = '0.1'

def gh_request(url, *args, **kwargs):
    BASE = r'https://api.github.com'
    r = requests.get(BASE + url, *args, **kwargs)
    if r.status_code != 200 and not int(r.headers['X-RateLimit-Remaining']):
        reset = datetime.fromtimestamp(int(r.headers['X-RateLimit-Reset']))
        raise requests.HTTPError('Rate limit exceeded! Blocked until {}'.format(reset))
    r.raise_for_status()
    return r


def repos(owner, repolist=None, page=1):
    if repolist is None:
        repolist = []
    r = gh_request('/users/{}/repos'.format(owner),
                   params={'per_page': 100, 'page': page})
    yield from iter(r.json())
    if r.links.get('next'):
        yield from repos(owner, repolist, page=page+1)


def main(*owners):
    results = []
    name_width = 4 # Length of 'Repo' header
    count_width = 5  # Length of 'Stars' header
    for owner in owners:
        for repo in repos(owner):
            stars_count = repo['stargazers_count']
            if stars_count:
                name = repo['full_name']
                results.append((name, stars_count))
                if len(name) > name_width:
                    name_width = len(name)
                if len(str(stars_count)) > count_width:
                    count_width = len(str(stars_count))

    results.sort(key=itemgetter(1), reverse=True)

    template = ' {:{w1}}   {:>{w2}} '
    for a, b in chain([('Repo', 'Stars'), ('=' * name_width, '=' * count_width)], results):
        print(template.format(a, b, w1=name_width, w2=count_width))


if __name__ == '__main__':
    if sys.argv[1:]:
        main(*sys.argv[1:])
    else:
        sys.exit('Usage: python ghstars.py owner [owner2 ...]')
