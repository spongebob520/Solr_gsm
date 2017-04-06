#! /usr/bin/python
# -*- coding: utf-8 -*-
#import pysolr
import os
from field.change_field import changeField
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://localhost:8983/solr/voice/'
top_file = '/work/voice_data/'

#for i in os.listdir(top_file):
def pysolrAddtxt(top_file,url):
    i = top_file.split('/')[-1]
    field_C = changeField()
    # txt文档没有第一行的表头，所以txt文档按照列post数据，每一列的索引键值在curl代码中的fieldnames定义
    if os.path.isdir(os.path.join(top_file)):#读出每个txt文件
        filename = os.path.join(top_file,"annotation",'%s.txt'%(i))
        if os.path.isfile(filename):
            # 判断是否有这个txt文件，有的话先删除，在post新的
            field_C.deleteIndex(i, "txt", url)
            with open(filename) as txt_file:
                for line in txt_file:#按行读txt文件
                    line = line.decode("utf-8")
                    line = line.strip(" \r\n")
                    fields = line.split("\t")
                    print int(len(fields))
                    if int(len(fields)) == int(2):
                        shell = "curl '"+ "http://localhost:8983/solr/voice/update?&" + "literal.belong=%s"%(i+"_txt") +  "&literal.type=txt&commit=true&separator=%09&escape=%5c&fieldnames=name,content'" + " --data-binary @%s -H 'Content-type:text/csv'"%(filename)
                        os.system("%s"%(shell))
                        break
                    elif int(len(fields)) == int(4):
                        shell = "curl '"+ "http://localhost:8983/solr/voice/update?&" + "literal.belong=%s"%(i+"_txt") +  "&literal.type=txt&commit=true&separator=%09&escape=%5c&fieldnames=name,begin,end,content'" + " --data-binary @%s -H 'Content-type:text/csv'"%(filename)
                        os.system("%s"%(shell))
                        break
                    else:
                        break
