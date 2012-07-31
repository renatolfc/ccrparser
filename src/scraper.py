#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys
import errno
import os.path
import urllib2
import datetime

try:
    import cPickle as pickle
except ImportError:
    import pickle

from CCRParser import CCRParser

LOGDIR = os.environ.get('SCRAPER_LOG_DIR', 'logs')
URLS = [('dutra', 'http://www.novadutra.com.br/'),
        ('spvias', 'http://www.spvias.com.br/'),
        ('ponte', 'http://www.ponte.com.br/'),
        ('vialagos', 'http://www.rodoviadoslagos.com.br/'),
        ('rodonorte', 'http://www.rodonorte.com.br/'),
        ('autoban', 'http://www.autoban.com.br/'),
        ('viaoeste', 'http://www.viaoeste.com.br/'),
        ('rodoanel', 'http://www.rodoaneloeste.com.br/')]
SUFFIX = '/servicos/BoletimOnline.aspx'

def utcnow():
    return datetime.datetime.utcnow()

def date_to_path(date):
    return reduce(os.path.join, [str(i) for i in [date.year, date.month,
        date.day] + ['%s:%s' % (date.hour, date.minute)]])

def check_sanity():
    if not os.path.exists(LOGDIR):
        os.makedirs(LOGDIR)
    else:
        if not os.path.isdir(LOGDIR):
            raise SystemExit(LOGDIR + ' exists, but is not a directory')
    for (highway, _) in URLS:
        path = os.path.join(LOGDIR, highway)
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            if not os.path.isdir(path):
                raise SystemExit(path + ' exists, but is not a directory')

def getpois(parser, url):
    try:
        page = urllib2.urlopen(url + SUFFIX)
        # parse the data and convert it to something we can use
        # FIXME: This 'utf-8' hard-coded here is a tragedy waiting to happen
        pois = list(parser.parse(unicode(page.read(), 'utf-8')))
        page.close()
        return pois
    except urllib2.URLError:
        return []

def createpath(filename):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError as error:
        if error.errno == errno.EEXIST:
            pass
        else:
            # Oops
            raise

def unlock(filename):
    lockname = filename + '.lock'
    os.unlink(lockname)

def lock(filename):
    lockname = filename + '.lock'
    open(lockname, 'w').close()

def storedata(pois, filename):
    # store the data
    lock(filename)
    fp = open(filename, 'w')
    pickle.dump(pois, fp)
    fp.close()
    unlock(filename)

def main(args):
    check_sanity()
    parser = CCRParser()
    path = date_to_path(utcnow())
    # download the data from the CCR site
    for (highway, url) in URLS:
        filename = os.path.join(LOGDIR, highway, path)
        pois = getpois(parser, url)
        createpath(filename)
        storedata(pois, filename)

if __name__ == '__main__':
    main(sys.argv[1:])

