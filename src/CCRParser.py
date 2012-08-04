#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function

from BeautifulSoup import BeautifulSoup
import re

unlikely_pattern = r'~~~======~~~::::,,,xpto~~~==='

class CCRParser(object):
    '''Simple parser for CCR's "BoletimOnline" page.

    This class parses the page and populates the pois attribute when it finds
    Points of Interest with low flow in the highway.

    '''

    poitag = 'div'
    poiattrs = 'box_postos'
    poicolumns = (u'stretch', u'traffic', u'lane', u'reason', u'observation',
            u'start', u'end')
    start = r'KM Inicial:\s*' + unlikely_pattern
    end = r'KM Final:\s*' + unlikely_pattern
    importantcolumns = (u'stretch', u'start', u'end', u'traffic')
    container = 'p'
    realstart = 'KM Inicial: '
    realend = 'KM Final: '

    def match_to_dict(self, match):
        d = {}
        for i, column in enumerate(self.poicolumns):
            try:
                tmp = match[i]
                colon = tmp.find(':') if column != u'stretch' else -1
                value = tmp[colon+1:].strip()
                d[column] = value if len(value) != 0 else u'-'
                try:
                    if column == u'start' or column == u'end':
                        d[column] = float(d[column].replace(',', '.'))
                except ValueError:
                    pass
            except IndexError:
                d[column] = u'-'
        if d == {}:
            return None
        for column in self.importantcolumns:
            if d[column] == u'-':
                return None
        return d

    def parse(self, page):
        alldata = []
        pagesoup = BeautifulSoup(page)
        boxes = pagesoup.findAll(self.poitag, self.poiattrs)
        for box in boxes:
            soup = BeautifulSoup(str(box))
            for p in soup.findAll(self.container):
                text = p.getText(unlikely_pattern)
                text = re.sub(self.start, self.realstart, text, flags = re.I)
                text = re.sub(self.end, self.realend, text, flags = re.I)
                alldata.append(text)
        for elem in alldata:
            elem = elem.split(unlikely_pattern)
            elem = filter(lambda e: len(e) != 0, elem)
            out = self.match_to_dict(elem)
            if out is not None:
                yield out

