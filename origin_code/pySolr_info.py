#! /usr/bin/python
# -*- coding: utf-8 -*-
#import pysolr

import os
import sys
from field.change_field import changeField
reload(sys)
sys.setdefaultencoding('utf-8')
top_file = '/work/voice_data/'
url = 'http://localhost:8983/solr/voice/'

for i in os.listdir(top_file):
    field_C = changeField()
    # 首先得到已有的fields
    fields_list = field_C.getField(url)
    if os.path.isdir(os.path.join(top_file,i)):#读出每个info文件
        filename = os.path.join(top_file,i,"%s.info"%(i))
        if os.path.isfile(filename):
            field_C.deleteIndex(i, "info", url)
            fields = []
            #在对数据curl之前检查field是否存在，不存在的话定义
            with open(filename) as infofile:
                for line in infofile:
                    line = line.decode("utf-8")
                    line.strip("\n")
                    fields = line.split("\t")
                    break
            for m in xrange(len(fields)):
                field_m = fields[m].strip()
                field_m.decode("utf-8")
                field_C.addField(field_m,fields_list,url)
                fields_list = field_C.getField(url)
                #print field_m
            print filename
            shell = "curl '"+ "http://localhost:8983/solr/voice/update?literal.belong=" + "%s"%(i+"_info") + "&literal.type=info&commit=true&separator=%09&escape=%5c'" + " --data-binary @%s -H 'Content-type:application/csv'"%(filename)
            os.system("%s"%(shell))
            
            

