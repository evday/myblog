# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-30 06:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='telephone',
            field=models.IntegerField(blank=True, null=True, verbose_name='手机号'),
        ),
    ]
