# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-16 13:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UnsafeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('some_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
