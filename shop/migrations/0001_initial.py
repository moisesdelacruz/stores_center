# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 18:18
from __future__ import unicode_literals

from django.db import migrations, models
import shop.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
                ('description', models.TextField()),
                ('logo', models.ImageField(upload_to=shop.models.content_file_name)),
                ('cover_image', models.ImageField(blank=True, upload_to=shop.models.content_file_name)),
                ('slug', models.SlugField(editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
