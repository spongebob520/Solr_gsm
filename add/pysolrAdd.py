#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
from field.change_field import changeField
import sys
import pysolr
from urllib2 import *
reload(sys)
sys.setdefaultencoding('utf-8')

# ****************************************************************#
# solrAdd类：
# 1、solrAddtxt()函数对txt数据建立索引（四列或者两列的格式化txt）；
# 2、solrAddinfo()函数对info数据建立索引；
# 3、solrAdddesc()函数对desc数据建立索引；
# 4、定义：add = solrAdd()，用于之后介绍。
# 5、最近更新：2017.1.19
# ****************************************************************#

class solrAdd:
    # ********************************************************************************************************************************#
    # 用法：add.solrAddtxt(data_path,url)
    # 参数：data_path为要建立索引的某份数据的地址，url是库的连接地址，链接到库，例：url = 'http://localhost:8983/solr/voice/'这是连接到库voice的地址
    # 结果：对data_path下annotation下对应的txt(如果存在且命名格式正确的话)建立索引
    # 说明：1、针对voice内的txt，因为voice内的txt是格式化的，分4列或两列，如果数据出现三列则会出现问题，
    #       2、对两列txt建立的字段分别为name和content，对四列建立的字段分别为name、begin、end、content，
    #       3、如果想要更换每列对应字段，除了对变量shell内容里的“&filenames=”进行更改，还要对初始化函数（change_file.py）的几个默认添加进行更改，
    # 最近更新：2017.1.19
    # ********************************************************************************************************************************#
    def solrAddtxt(self,top_file,url):
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
                            shell = "curl '"+ url+"update?&" + "literal.belong=%s"%(i+"_txt") +  "&literal.type=txt&commit=true&separator=%09&escape=%5c&fieldnames=name,content'" + " --data-binary @%s -H 'Content-type:text/csv'"%(filename)
                            os.system("%s"%(shell))
                            break
                        elif int(len(fields)) == int(4):
                            shell = "curl '"+ url+"update?&" + "literal.belong=%s"%(i+"_txt") +  "&literal.type=txt&commit=true&separator=%09&escape=%5c&fieldnames=name,begin,end,content'" + " --data-binary @%s -H 'Content-type:text/csv'"%(filename)
                            os.system("%s"%(shell))
                            break
                        else:
                            break


    # ********************************************************************************************************************************#
    # 用法：add.solrAddinfo(data_path,url)
    # 参数：data_path为要建立索引的某份数据的地址，url是库的连接地址，链接到库，例：url = 'http://localhost:8983/solr/voice/'这是连接到库voice的地址
    # 结果：对data_path下对应的info(如果存在且命名格式正确的话)建立索引
    # 说明：1、对info文件建立索引，默认是按照第一行为索引字段（field）的，如果缺失字段会自动添加
    #       2、可能会出现的问题，如果第一行是5列，之后每行为4列，即一列内容为空，最好空的一列有空格符，否则可能出现索引内容无法匹配，导致数据无法post全面
    # 最近更新：2017.1.19
    # ********************************************************************************************************************************#
    def solrAddinfo(self,top_file, url):
        i = top_file.split('/')[-1]
        field_C = changeField()
        # 首先得到已有的fields
        fields_list = field_C.getField(url)
        if os.path.isdir(os.path.join(top_file)):#读出每个info文件
            filename = os.path.join(top_file,"%s.info"%(i))
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
                shell = "curl '"+ url+"update?literal.belong=" + "%s"%(i+"_info") + "&literal.type=info&commit=true&separator=%09&escape=%5c'" + " --data-binary @%s -H 'Content-type:application/csv'"%(filename)
                os.system("%s"%(shell))

    # ******************************************************************************************************#
    # 用法：add.solrAdddesc(data_path,url)
    # 参数：data_path为要建立索引的某份数据的地址，url是库的连接地址，链接到库，例：url = 'http://localhost:8983/solr/voice/'这是连接到库voice的地址
    # 结果：对data_path下对应的desc(如果存在且命名格式正确的话)建立索引
    # 说明：1、对desc文件建立索引，默认是按照第一列为索引字段（field）的，如果缺失字段会自动添加
    #       2、voice、medical数据都可以用，只要注意data_path和url地址即可
    # 最近更新：2017.1.19
    # ******************************************************************************************************#
    def solrAdddesc(self,top_file,url):
        i = top_file.split('/')[-1]
        title_list = []
        content_list = []
        dics = {}
        field_C = changeField()
        solr = pysolr.Solr(url, timeout=10)
        # 首先得到已有的fields
        fields_list = field_C.getField(url)
        if os.path.isdir(os.path.join(top_file)):#读出每个desc文件
            filename = os.path.join(top_file,'%s.desc'%(i))
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
                        else:
                            fields = line.split("  ")
                            if len(fields)>1:
                                field_C.addField(fields[0].strip("："), fields_list, url)
                                fields_list = field_C.getField(url)
                                title_list.append(fields[0].strip("："))
                                content_list.append(fields[1])
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


if __name__ == '__main__':
    url_o = 'http://localhost:8983/solr/text/'
    top = '/work/voice_data/'
    add = solrAdd()
    for name in os.listdir(top):
        if os.path.isdir(os.path.join(top,name)):
            add.solrAdddesc(os.path.join(top,name),url_o)
            add.solrAddinfo(os.path.join(top,name),url_o)
            add.solrAddtxt(os.path.join(top,name),url_o)
