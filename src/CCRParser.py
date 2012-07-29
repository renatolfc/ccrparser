#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function

from HTMLParser import HTMLParser
import re

class CCRParser(HTMLParser):
    '''Simple parser for CCR's "BoletimOnline" page.

    This class parses the page and populates the pois attribute when it finds
    Points of Interest with low flow in the highway.

    '''

    poitag = 'div'
    poiattrs = ('class', 'box_postos')
    poicolumns = ('stretch', 'traffic', 'lane', 'reason', 'observation',
            'start', 'end')
    poiregex = re.compile(r'^(?P<%s>.*)$\s*'
            r'^.*:\s+(?P<%s>.*)$\s*'
            r'^.*:\s+(?P<%s>.*)$\s*'
            r'^.*:\s+(?P<%s>.*)$\s*'
            r'^.*:\s+(?P<%s>.*)$\s*'
            r'^.*:\s+(?P<%s>.*)$\s*'
            r'^.*:\s+(?P<%s>.*)$' % poicolumns, re.MULTILINE|re.DOTALL)

    def __init__(self):
        HTMLParser.__init__(self)
        self.alldata = []
        self.workstr = ''
        self.indiv = False

    def handle_starttag(self, tag, attrs):
        if tag == self.poitag and self.poiattrs in attrs:
            self.indiv = True
            self.workstr = ''

    def handle_data(self, data):
        if self.indiv:
            data = data.strip()
            if data is not '':
                self.workstr += data.strip() + '\n'

    def handle_endtag(self, tag):
        if tag == self.poitag and self.indiv:
            self.indiv = False
            self.alldata.append(self.workstr)

    def match_to_dict(self, match):
        d = {}
        for column in self.poicolumns:
            try:
                d[column] = match.group(column)
            except IndexError:
                d[column] = '-'
        return d

    def parse(self, page):
        self.alldata = []
        self.feed(page)
        matches = (self.poiregex.match(poi) for poi in self.alldata)
        return (self.match_to_dict(match) for match in matches if match is not None)

