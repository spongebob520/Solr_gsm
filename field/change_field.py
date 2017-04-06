#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from urllib2 import *
import pysolr
reload(sys)
sys.setdefaultencoding('utf-8')

#****************************************************************#
# changeField类：
# 1、getField()函数得到库的fields列表；
# 2、addField()函数判断field是否在库中已有定义，没有的话添加；
# 3、deleteField()函数删除不想要的field；
# 4、deleteIndex()函数删除doc；
# 5、initializtion()函数用来初始化新创建的库；
# 6、定义：field = changeField()，用于之后介绍。
# 7、最近更新：2017.1.19
#****************************************************************#

class changeField:
        # ****************************************************************************************************#
        # 用法：list = field.initializtion(url)
        # 参数：url是库的连接地址，链接到库，例：url = 'http://localhost:8983/solr/voice/'这是连接到库voice的地址
        # 结果：对新建立的库的配置文件进行初始化，创建一些必要的定义，只需一次就可以
        # 最近更新：2017.1.19
        # ****************************************************************************************************#
        def initializtion(self,url):
                field = changeField()
                fields_list = field.getField(url)
                #两个默认的
                field.addField("text", fields_list, url)
                field.addField("type",fields_list,url)
                #用于txt的初始化，两列或四列
                field.addField("name", fields_list, url)
                field.addField("content", fields_list, url)
                field.addField("begin", fields_list, url)
                field.addField("end", fields_list, url)
                #每个索引都有，保存数据ID
                field.addField("belong", fields_list, url)

        # ****************************************************************************************************#
        # 用法：list = field.getField(url)
        # 参数：url是库的连接地址，链接到库，例：url = 'http://localhost:8983/solr/voice/'这是连接到库voice的地址
        # 结果：得到一个list，list是库配置文件中已定义的field
        # 最近更新：2017.1.19
        # ****************************************************************************************************#
        def getField(self,url_o):
                #注意：true和false的定义不能注释，在读取fields的json内容时，为了得到字典，需要对字符串中的true和false定义
                true = "true"
                false = "false"
                name = []
                shell = 'curl ' + url_o + 'schema/fields?wt=json'
                middle = os.popen(shell)
                field_m = eval(middle.read())
                fields = field_m["fields"]
                for i in xrange(len(fields)):
                        name.append(fields[i]["name"].strip())
                return name

        #判断读入字段是否在fields里，如果不在的话添加字段
        # **********************************************************************************************************************************#
        # 用法：field.addField(field_name,list,url)
        # 参数：field_name即要检查的字段名字，list即库以有field的合集，url是库的连接地址，例：url = 'http://localhost:8983/solr/voice/'这是连接到库voice的地址
        # 结果：检查field_name是否已在配置文件中定义过，没有的话同时添加field和copyfiled
        # 说明：1、代码中单独列出了对text字段和type字段的定义，text的作用是用来映射其他字段，type只需要建立索引不需要存储，所以单独定义；
        #       2、目前我们对field定义时，默认格式为text_general，并且都建立索引且存储，即对应字段按照文本存储，并且可以显示出来。
        # 最近更新：2017.1.19
        # **********************************************************************************************************************************#
        def addField(self,check_field,fields_list,link):
                url = link + "schema"
                if check_field in  "text":
                        shell = "curl -X POST -H 'Content-type:application/json' --data-binary '" + '{"add-field":{"name":"' + '%s'%(check_field) + '","type":"text_general","stored":false ,"indexed":true ,"multiValued":true'+"}}' %s"%(url)
                        os.system("%s"%(shell))
                elif check_field in "type":
                        shell = "curl -X POST -H 'Content-type:application/json' --data-binary '" + '{"add-field":{"name":"' + '%s' % (check_field) + '","type":"text_general","stored":false ,"indexed":true ' + "}}' %s" % (
                        url)
                        os.system("%s" % (shell))
                elif check_field in fields_list:
                        pass
                else:
                        #添加field和copyfield
                        shell = "curl -X POST -H 'Content-type:application/json' --data-binary '" + '{"add-field":{"name":"' + '%s'%(check_field) + '","type":"text_general","stored":true ,"indexed":true ' + "},"+'"add-copy-field":{"dest":"text","source":' + '"%s"'%(check_field)+"}}' %s"%(url)
                        os.system(" %s " % (shell))
                        print check_field

        #给新加入的字段添加高亮，未完成
        def addHighlight(self,newField,link):
                pass

        #删除某个field和对应的copyfield
        # ****************************************************************#
        # 用法：field.deleteField(field_name,url)
        # 参数：field_name即要删除的字段名字，url是库的连接地址，例：url = 'http://localhost:8983/solr/voice/
        # 结果：同时删除了filed_name的copyfield和field定义，一定要先删除copyfield，才能删除field
        # 最近更新：2017.1.19
        # ****************************************************************#
        def deleteField(self,d_Field,link):
                url = link + "schema"
                shell_c = "curl -X POST -H 'Content-type:application/json' --data-binary '" + '{"delete-copy-field":{"dest":"text","source":' + '"%s"' % (d_Field) + "}}' %s" % (url)
                os.system(shell_c)
                shell = "curl -X POST -H 'Content-type:application/json' --data-binary '"+'{"delete-field" : { "name":"'+"%s"%(d_Field)+'" }}'+"' %s"%(url)
                os.system(shell)

        #根据每份数据的数据ID以及数据的所属类别，再post数据之前先将原来以后的数据删除
        # **************************************************************************************************************************************#
        # 用法：field.deleteIndex(data_ID,data_type,url)
        # 参数：data_ID为每份数据对应的ID，data_type即想要删除的这份数据里的文件类型（info,txt,desc），url是库的连接地址，例：url = 'http://localhost:8983/solr/voice/
        # 结果：删除data_ID数据内data_type类型的所有索引
        # 说明：现在只完成了txt、info、desc数据的删除
        # 最近更新：2017.1.19
        # **************************************************************************************************************************************#
        def deleteIndex(self,ID,type,url_o):
                solr = pysolr.Solr(url_o, timeout=10)
                if "desc" in type:
                        url = url_o + 'select?q=%s&wt=python&fq=%s' % (ID, type)
                        connection = urlopen(url)
                        response = eval(connection.read())
                        for document in response['response']['docs']:
                                if document['belong'][0] in ID:
                                        id = document["id"]
                                        solr.delete(id=id)
                                        break
                elif "txt" in type or "info" in type:
                        m = ID + "_%s"%(type)
                        url = url_o + 'select?q=%s&wt=python&fq=%s' % (m, type)
                        connection = urlopen(url)
                        response = eval(connection.read())
                        for document in response['response']['docs']:
                                print m
                                print ID
                                if document['belong'][0] in m:
                                        solr.delete(q=m)
                                        break
                else:
                        pass



if __name__ == '__main__':
        # url和list只是测试的时候用的
        url = 'http://localhost:8983/solr/voice/'
        list = []
        field = changeField()
        list =  field.getField(url)
        #print list[0]
        if u'角度' in list:
                print "True"
        else:
                print list[0].strip()
        #field.deleteField(u'你好',url)





