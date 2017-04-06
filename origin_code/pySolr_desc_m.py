#! /usr/bin/python
# -*- coding: utf-8 -*-
import pysolr
import os
# Setup a Solr instance. The timeout is optional.
import sys #要重新载入sys。因为 Python 初始化后会删除 sys.setdefaultencoding 这个方 法
reload(sys)
sys.setdefaultencoding('utf-8')
solr = pysolr.Solr('http://localhost:8983/solr/medical', timeout=10)
# How you'd index data.
top_file = '/work/medical/data'
title_list = []
content_list = []
for i in os.listdir(top_file):
    if os.path.isdir(os.path.join(top_file,i)):#读出每个desc文件
        filename = os.path.join(top_file,i,'%s.desc'%(i))
        if os.path.isfile(filename):
            with open(filename) as desc_file:
                for line in desc_file:#按行读desc文件
                    line = line.decode("utf-8")
                    line = line.strip(" \r\n")
                    fields = line.split("\t")
                    if len(fields)>1:
                        title_list.append(fields[0].strip("："))
                        content_list.append(fields[1])
                        #solr.add([{"id":"%s"%(i),"%s"%(fields[0]):"%s"%(fields[1]),}])
                    else:
                        fields = line.split("  ")
                        if len(fields)>1:
                            title_list.append(fields[0].strip("："))
                            content_list.append(fields[1])
                            #solr.add([{"id": "%s" % (i), "%s" % (fields[0]): "%s" % (fields[1]), }])
                        else :
                            title_list.append(fields[0].strip("："))
                            content_list.append("")
                solr.add([{u"%s" % (title_list[0]): u"%s" % (content_list[0]),
                           u"%s" % (title_list[1]): u"%s" % (content_list[1]),u"%s" % (title_list[2]): u"%s" % (content_list[2]),
                           u"%s" % (title_list[3]): u"%s" % (content_list[3]),u"%s" % (title_list[4]): u"%s" % (content_list[4]),
                           u"%s" % (title_list[5]): u"%s" % (content_list[5]),u"%s" % (title_list[6]): u"%s" % (content_list[6]),
                           u"%s" % (title_list[7]): u"%s" % (content_list[7]),u"%s" % (title_list[8]): u"%s" % (content_list[8]),
                           u"%s" % (title_list[9]): u"%s" % (content_list[9]),u"%s" % (title_list[10]): u"%s" % (content_list[10]),
                           u"%s" % (title_list[11]): u"%s" % (content_list[11]),u"%s" % (title_list[12]): u"%s" % (content_list[12]),
                           u"%s" % (title_list[13]): u"%s" % (content_list[13]),u"%s" % (title_list[14]): u"%s" % (content_list[14]),
                           u"%s" % (title_list[15]): u"%s" % (content_list[15]),"type": "desc" ,}])
                print filename
                title_list = []
                content_list = []
# solr.add([
#     {
#         "id": "doc_1",
#         "title": "A test document",
#     },
#     {
#         "id": "doc_2",
#         "title": "The Banana: Tasty or Dangerous?",
#     },
# ])
