#! /usr/bin/python
# -*- coding: utf-8 -*-

from urllib2 import *
from API.portApi import API
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


if __name__ == '__main__':
    url = ''
    type = ''
    q = ''
    fq = ()
    get = API()
    if len(sys.argv) < 4:
        print "Usage:python "  + sys.argv[0] + u" <需要更新的库地址>" + u" <输出格式>"+ u" <主检查字段>"+ u" <匹配字段（可无）>"
        print "Example:python API_run.py  http://localhost:8983/solr/voice/ json dinobot_shenjingwaike_20160418_txt 肌肉"
        exit(-1)
    else:
        url = sys.argv[1]
        type = sys.argv[2]
        q = sys.argv[3]
    if len(sys.argv) > 4:
        for i in range(4,len(sys.argv)):
            m = (sys.argv[i],)
            fq += m
        dict = get.getPort(url, type, q,*fq)
        print dict
    else:
        dict = get.getPort(url, type, q)
        print dict