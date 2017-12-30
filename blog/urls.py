#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-30,15:36"

from django.conf.urls import url
from django.contrib import admin


from blog import views

urlpatterns = [
    url (r"^(?P<username>.*)/(?P<condition>category|tag|date)/(?P<para>.*)/$",views.homeSite),
    url (r"^(?P<username>.*)/$",views.homeSite,name = "aaa"),


]