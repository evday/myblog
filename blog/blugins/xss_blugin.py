#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Author:沈中秋
#date:"2017-11-29,0:11"

from bs4 import BeautifulSoup
def filter_xss(html_str):

    # 创建安全标签列表
    valid_tag_str =  ["p","div","a", "img", "html", "body", "br", "strong", "b","hr"]
    # 创建安全属性字典
    valid_dict = {"p": ["id", "class"], "div": ["id", "class"]}

    soup = BeautifulSoup(html_str,"html.parser")#实例化soup对象，需要指定两个参数，html字符串，和引擎
    for ele in soup.find_all():
        #过滤非法标签
        if ele.name not in valid_tag_str:
            ele.decompose()   #删除
        else:
            attrs = ele.attrs #获取属性字典
            l = []
            for k in attrs:#如果k 没有在安全属性字典中，就添加到列表中
                if k not in valid_dict[ele.name]:
                    l.append(k)
            for i in l:#循环遍历这些k,将他们删除
                del attrs[i]
    return soup.decode() #返回验证过得soup对象

