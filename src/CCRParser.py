#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function

from BeautifulSoup import BeautifulSoup, UnicodeDammit
import re

class CCRParser(object):
    '''Simple parser for CCR's "BoletimOnline" page.

    This class parses the page and populates the pois attribute when it finds
    Points of Interest with low flow in the highway.

    '''

    poitag = 'div'
    poiattrs = 'box_postos'
    poicolumns = (u'stretch', u'traffic', u'lane', u'reason', u'observation',
            u'start', u'end')
    poiregex = re.compile(r'^(?P<%s>.*)$\s*'
            r'^.*:\s+(?P<%s>.*)$\s*'
            r'^.*:\s+(?P<%s>.*)$\s*'
            r'^.*:\s+(?P<%s>.*)$\s*'
            r'^.*:\s+(?P<%s>.*)$\s*'
            r'^.*:\s+(?P<%s>.*)$\s*'
            r'^.*:\s+(?P<%s>.*)$' % poicolumns, re.MULTILINE|re.DOTALL)

    def match_to_dict(self, match):
        d = {}
        for column in self.poicolumns:
            try:
                d[column] = match.group(column)
            except IndexError:
                d[column] = '-'
        return d

    def parse(self, page):
        alldata = []
        pagesoup = BeautifulSoup(page)
        boxes = pagesoup.findAll(self.poitag, self.poiattrs)
        for box in boxes:
            soup = BeautifulSoup(str(box))
            for p in soup.findAll('p'):
                alldata.append(p.getText('\n'))
        matches = (self.poiregex.match(poi) for poi in alldata)
        return (self.match_to_dict(match) for match in matches if match is not None)

