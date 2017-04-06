#! /usr/bin/python
# -*- coding: utf-8 -*-

from urllib2 import *
from API.portApi import API
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def getPort(url_o,out_type,q,*fq):
    fqs = ''
    print fq
    for i in xrange(len(fq)):
        fqs += '&fq=%s'%(fq[i])
    if len(fqs) == 0:
        url = url_o + 'select?q=%s' % (q)  + '&indent=on&wt=%s' % (out_type)
    else:
        url = url_o + 'select?q=%s' % (q) +'%s'%(fqs)+ '&indent=on&wt=%s'%(out_type)
    print url
    connection = urlopen(url)
    response = eval(connection.read())
    return response



if __name__ == '__main__':
    url = "http://localhost:8983/solr/voice/"
    print getPort(url,"json","dinobot_shenjingwaike_20160418_txt",u"肌肉")