#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys
import json
import errno
import filecmp
import os.path
import urllib2
import datetime

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
    path = '%d %.2d %.2d '.replace(' ', os.sep) % (date.year, date.month, date.day)
    return path + '%.2d:%.2d' % (date.hour, date.minute)

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
    # FIXME: Define a better way to determine the file path

    lock(filename)

    fp = open(filename, 'w')
    fp.write(json.dumps(pois, sort_keys=True, indent=2)+'\n')
    fp.close()

    unlock(filename)

    # If the current file is equal to the previous one, we can just link this
    # file to that
    current = [int(i) for i in os.path.basename(filename).split(':')]
    if current[0] == 0 and current[1] == 0:
        # We don't want to handle the case where we have to link to a file in
        # another directory, so if it is midnight, we'll accept the burden of
        # having a duplicated file.
        return
    elif current[1] == 0:
        previous = str(current[0]-1) + ':59'
    else:
        previous = str(current[0]) + ':' + str(int(current[1])-1)
    previous = os.path.join(os.path.dirname(filename), previous)
    if os.path.exists(previous) and filecmp.cmp(filename, previous):
        # Files are equal, let's just link them
        lock(filename)
        os.unlink(filename)
        os.link(previous, filename)
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

