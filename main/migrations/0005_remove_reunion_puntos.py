# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-23 01:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20160519_1631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reunion',
            name='puntos',
        ),
    ]
