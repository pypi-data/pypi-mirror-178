# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-04 04:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fec_dbsync', '0002_auto_20180530_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalaccount',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
