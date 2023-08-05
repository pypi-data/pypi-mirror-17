# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-16 13:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('unsafe_migrations', '0002_unsafemodel_field_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='unsafemodel',
            name='safe_field',
            field=models.IntegerField(null=True),
        ),

        migrations.AddField(
            model_name='unsafemodel',
            name='field_added',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),

        migrations.AlterField(
            model_name='unsafemodel',
            name='field_added',
            field=models.PositiveIntegerField(default=10),
            preserve_default=False
        ),

        migrations.RenameField(
            model_name='unsafemodel',
            old_name='field_added',
            new_name='field_renamed'
        ),

        migrations.RemoveField(
            model_name='unsafemodel',
            name='field_renamed',
        ),

        migrations.DeleteModel('unsafemodel'),
    ]
