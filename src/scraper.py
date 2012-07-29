#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys
import os.path
import urllib2
import datetime

try:
    import cPickle as pickle
except ImportError:
    import pickle

from DutraParser import DutraParser

LOGDIR = os.environ.get('SCRAPER_LOG_DIR', 'logs')
URL = 'http://www.novadutra.com.br/servicos/BoletimOnline.aspx'

def isonow():
    return datetime.datetime.utcnow().isoformat()

def check_sanity():
    if not os.path.exists(LOGDIR):
        os.makedirs(LOGDIR)
    else:
        if not os.path.isdir(LOGDIR):
            raise SystemExit(LOGDIR + ' exists, but is not a directory')

def main(args):
    check_sanity()
    # download the data from the CCR site
    parser = DutraParser()
    page = urllib2.urlopen(URL)
    # parse the data and convert it to something we can use
    pois = parser.parse(page.read())
    page.close()
    # store the data
    filename = os.path.join(LOGDIR, isonow())
    lockname = filename + '.lock'
    open(lockname, 'w').close() # Create a lockfile
    fp = open(filename, 'w')
    pickle.dump(list(pois), fp)
    fp.close()
    os.unlink(lockname)

if __name__ == '__main__':
    main(sys.argv[1:])

