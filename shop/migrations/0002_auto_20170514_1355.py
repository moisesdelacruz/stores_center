# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-14 17:55
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='slug',
            field=models.SlugField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shop',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]