#! /usr/bin/python
# -*- coding: utf-8 -*-
import pysolr
import os
import sys #要重新载入sys。因为 Python 初始化后会删除 sys.setdefaultencoding 这个方 法
reload(sys)
sys.setdefaultencoding('utf-8')
solr = pysolr.Solr('http://localhost:8983/solr/medical')
top_file = '/work/medical/data'
content = ''
for i in os.listdir(top_file):
    if os.path.isdir(os.path.join(top_file,i)):
        for m in os.listdir(os.path.join(top_file,i)):
            if os.path.isdir(os.path.join(top_file,i,m)):#读出每个txt文件
                for n in os.listdir(os.path.join(top_file,i,m)):
                    if os.path.isfile(os.path.join(top_file,i,"plaintext",n)):
                        filename = os.path.join(top_file,i,m,n)
                        type_c = 'plaintext_txt'
                        print filename
                        f = open(filename, "r")
                        content = f.read()
                        f.close()
                        print "done1"
                        solr.add([{"belong":"%s"%(i),"content":"%s"%(content),"name":"%s"%(n),"type":"%s"%(type_c),}])
                        print "done2"
                        content = ''
                        
