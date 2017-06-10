# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-10 20:49
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_product_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
