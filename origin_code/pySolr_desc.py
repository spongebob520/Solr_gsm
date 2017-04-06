#! /usr/bin/python
# -*- coding: utf-8 -*-
import pysolr
import os
from field.change_field import changeField
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
url = 'http://localhost:8983/solr/voice/'
#solr = pysolr.Solr('http://localhost:8983/solr/voice', timeout=10)
top_file = '/work/voice_data/'

for i in os.listdir(top_file):
    title_list = []
    content_list = []
    dics = {}
    field_C = changeField()
    solr = pysolr.Solr('http://localhost:8983/solr/voice', timeout=10)
    # 首先得到已有的fields
    fields_list = field_C.getField(url)
    if os.path.isdir(os.path.join(top_file,i)):#读出每个desc文件
        filename = os.path.join(top_file,i,'%s.desc'%(i))
        if os.path.isfile(filename):
            # 判断是否有这个desc文件，有的话先删除，在post新的
            field_C.deleteIndex(i, "desc", url)
            with open(filename) as desc_file:
                for line in desc_file:#按行读desc文件
                    line = line.decode("utf-8")
                    line = line.strip(" \r\n")
                    fields = line.split("\t")
                    if len(fields)>1:
                        #判断是否有field，没有的话创建field，并且更新field_list
                        field_C.addField(fields[0].strip("："),fields_list,url)
                        fields_list = field_C.getField(url)
                        title_list.append(fields[0].strip("："))
                        content_list.append(fields[1])
                        #solr.add([{"id":"%s"%(i),"%s"%(fields[0]):"%s"%(fields[1]),}])
                    else:
                        fields = line.split("  ")
                        if len(fields)>1:
                            field_C.addField(fields[0].strip("："), fields_list, url)
                            fields_list = field_C.getField(url)
                            title_list.append(fields[0].strip("："))
                            content_list.append(fields[1])
                            #solr.add([{"id": "%s" % (i), "%s" % (fields[0]): "%s" % (fields[1]), }])
                        else :
                            if fields[0].strip("：") in fields_list:
                                title_list.append(fields[0].strip("："))
                                content_list.append("")
                            else:
                                pass
                for m in xrange(len(title_list)):
                    dics[title_list[m]] = "%s"%(content_list[m])
                dics["type"] = "desc"
                dics["belong"] = "%s"%(i)
                docs = [dics]
                solr.add(docs)
                print filename

