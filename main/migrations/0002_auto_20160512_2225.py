# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-12 20:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documentos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documentos', models.FileField(blank=True, null=True, upload_to='documents/%Y/%m/%d')),
            ],
        ),
        migrations.RemoveField(
            model_name='punto',
            name='documentos',
        ),
        migrations.AddField(
            model_name='documentos',
            name='punto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Punto'),
        ),
    ]
