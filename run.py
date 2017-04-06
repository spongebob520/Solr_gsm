#! /usr/bin/python
# -*- coding: utf-8 -*-
import pysolr
import os
from urllib2 import *
from field.change_field import changeField
from add.pysolrAdd import solrAdd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage:python "  + sys.argv[0] + u" <最顶层目录>" + u" <需要更新的库地址>"
        print "Example:python run.py /work/voice_data/ http://localhost:8983/solr/voice/"
        exit(-1)
    else:
        top = sys.argv[1]
        url_o = sys.argv[2]
    add = solrAdd()
    field_C = changeField()
    # field_C.initializtion(url_o)
    for name in os.listdir(top):
        if os.path.isdir(os.path.join(top, name)):
            add.solrAdddesc(os.path.join(top, name), url_o)
            add.solrAddinfo(os.path.join(top, name), url_o)
            add.solrAddtxt(os.path.join(top, name), url_o)