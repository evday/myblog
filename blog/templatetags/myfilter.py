#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:沈中秋
# date:"2017-11-29,19:13"
import datetime

from django import template
from django.utils.safestring import mark_safe

register = template.Library()  # register 是固定的，不能改变


@register.filter
def chardAge(time):

    # 时间对象可以直接做减法直接得到我们想要的结果，用时间戳的话还要转换，很麻烦
    #time 本身就是一个时间对象，直接做减法
    ret = datetime.datetime.now() - time.replace(tzinfo=None)

    ret = str(ret)[:-17]
    return mark_safe(ret)
