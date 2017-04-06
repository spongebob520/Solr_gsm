#! /usr/bin/python
# -*- coding: utf-8 -*-
from urllib2 import *
import sys
import pysolr
reload(sys)
sys.setdefaultencoding('utf-8')


# ****************************************************************#
# API类：
# 1、getPort()函数得到一个json或者xml或者python；
# 2、定义：port = API()。
# 3、最近更新：2017.1.19
# ****************************************************************#
class API:
    # *********************************************************************************************************************#
    # 用法：dict = port.getPort(q,url,type,*fq)
    # 参数：q为查询的主字段；url是库的连接地址，例：url = 'http://localhost:8983/solr/voice/'连接到voice库的地址；
    #       type为查询结果希望输出的格式，常用的有json，xml，python，ruby，php；*fq为过滤查询，是一个主元，根据输入
    #        参数的数量变化，是在主字段q下进一步匹配。
    # 结果：得到查询结果，以type类型保存在字典dict中
    # 说明：1、主字段内容q比较重要，一般是数据ID的话查询比较准确，如果想得到某数据的txt(info)数据，q设置为“数据ID_txt(info)”，
    #          查询desc的话q设置为数据ID就可以了，设置一个fq为desc；
    #       2、solr在创建库之后/serve/solr/colection/conf/solrconfig.xml内/select默认显示是10个document，但有的时候我们的数据
    #          docs数远远超过10，所以要手动更改一下。
    # 最近更新：2017.1.19
    # *********************************************************************************************************************#
    def getPort(self,url_o,out_type,q,*fq):
        fqs = ''
        print fq
        for i in xrange(len(fq)):
            m = quote(fq[i])
            fqs += '&fq=%s' % (m)
        if len(fqs) == 0:
            url = url_o + 'select?q=%s' % (q)  + '&indent=on&wt=%s' % (out_type)
        else:
            url = url_o + 'select?q=%s' % (q) +'%s'%(fqs)+ '&indent=on&wt=%s'%(out_type)
        print url
        connection = urlopen(url)
        response = eval(connection.read())
        return response


if __name__ == '__main__':
    pass