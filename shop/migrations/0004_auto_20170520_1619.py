# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-20 20:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20170514_1402'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shop',
            old_name='user',
            new_name='owner',
        ),
    ]