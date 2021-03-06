#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-30,15:36"

from django.conf.urls import url
from django.contrib import admin


from blog import views

urlpatterns = [
    url(r"^article_comment/$",views.article_comment),
    url(r"^poll/$",views.poll),
    url(r"^backend/$",views.backendIndex),
    url (r"^backend/addArticle/$",views.addArticle),
    url (r"^(?P<username>.*)/articles/(?P<article_id>\d+)/$",views.articleDetail,name = "article_detail"),
    url (r"^(?P<username>.*)/(?P<condition>category|tag|date)/(?P<para>.*)/$",views.homeSite),
    url (r"^(?P<username>.*)/$",views.homeSite,name = "aaa"),


]