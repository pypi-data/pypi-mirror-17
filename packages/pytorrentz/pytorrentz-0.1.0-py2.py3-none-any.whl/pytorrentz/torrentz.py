#!/usr/bin/python

'''
Python module for searching torrentz2.eu

Based on https://github.com/dannvix/torrentz-magdl
'''

from __future__ import unicode_literals
import re
import requests
from bs4 import BeautifulSoup
from pytorrentz.exceptions import *

try:
    # Python 3 and later
    from urllib.parse import urlencode, quote_plus
    from urllib.error import HTTPError
except ImportError:
    # Python 2
    from urllib import urlencode, quote_plus
    from urllib2 import HTTPError

class BASE(object):
    eu = 'https://torrentz2.eu/'
    proxy = 'https://torrentzeu.to/'
    # Try eu site, fallback to proxy site
    try:
        domain = eu
        requests.get(eu).status_code
    except HTTPError as e:
        domain = proxy
    ANY = '{}any'.format(domain)
    GOOD = '{}search'.format(domain)
    VERIFIED = '{}verified'.format(domain)


class ORDER(object):
    peers = '?f='
    size = 'S?f='
    date = 'A?f='
    rating = 'N?f='


class Torrent(object):
    def __init__(self, sha1, title, size, seeds, peers):
        self.sha1 = sha1
        self.title = title
        self.size = size
        self.seeds = seeds
        self.peers = peers

    def __repr__(self):
        return _valid_encoding('<Torrent(title={title})>'.format(title=self.title))

    def __str__(self):
        return _valid_encoding(self.title)

    def __unicode__(self):
        return self.title

    def __bool__(self):
        return bool(self.sha1)

    def __nonzero__(self):
        return bool(self.sha1)

    def get_magnet_uri(self):
        '''
        Build a magnet uri from sha1 and trackers

        Returns:
            (str) magnet uri
        '''
        # Retrieve tracker list from Torrentz
        url = BASE.domain + self.sha1
        html = requests.get(url).text
        trackers = re.findall(r'<a[^<>]*href="/tracker[^<>]*"[^<>]*>(?P<tracker>[^<>]*)</a>', html)

        # Build magnet links
        dn = urlencode(dict(dn=self.title))
        trs = '&'.join(map(lambda t: urlencode(dict(tr=t)),
                                                      trackers))
        uri = 'magnet:?xt=urn:btih:{sha1}&{dn}&{trs}'.format(sha1=self.sha1,
                                                             dn=dn,
                                                             trs=trs)
        return str(uri)


def _parse_torrents(soup):
    results = []
    dl = soup.find_all('dl')
    for item in dl:
        try:
            dt = item.find('dt')
            a = dt.find('a')
            dd = item.find('dd')
            span = dd.find_all('span')
            size = span[2].text
            seeds = span[3].text
            peers = span[4].text

            results.append(Torrent(
                sha1 = re.findall(r'^/(?P<sha1>[0-9a-f]+)$', a.get('href'))[0],
                title = a.text,
                size = size,
                seeds = seeds,
                peers = peers))
        except IndexError as e:
            print('index error')
            next
    return results


def _valid_encoding(text):
    if not text:
        return
    if sys.version_info > (3,):
        return text
    else:
        return unicode(text).encode('utf-8')


def search(query, quality='good', order='peers', limit=20):
    '''
    Search torrentz.eu

    Args:
        query (str)             -- Search term(s)
        quality (Optional[str]) -- 'any' | 'good' | 'verified'
        order (Optional[str])   -- 'peers' | 'size' | 'date' | 'rating'
        limit (Optional[int])   -- Maximum number of results to return

    Returns:
        (list) pytorrentz.Torrent objects
    '''

    if quality == 'any':
        url = BASE.ANY
    elif quality == 'good':
        url = BASE.GOOD
    elif quality == 'verified':
        url = BASE.VERIFIED
    else:
        raise KeywordError("quality keyword argument must be one of "
                           "('any' | 'good' | 'verified')")

    if order == 'peers':
        url = url + ORDER.peers
    elif order == 'size':
        url = url + ORDER.size
    elif order == 'date':
        url = url + ORDER.date
    elif order == 'rating':
        url = url + ORDER.rating
    else:
        raise KeywordError("order keyword argument must be one of "
                           "('peers' | 'size' | 'date' | 'rating')")

    params = quote_plus(query.encode('UTF-8'))
    html = requests.get(url + params).text
    soup = BeautifulSoup(html, 'lxml')
    items = _parse_torrents(soup)
    return items[:limit]
