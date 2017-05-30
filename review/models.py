# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from product.models import Product, IntegerRangeField
from django.contrib.auth.models import User

# Create your models here.

class Review(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    rating = IntegerRangeField(max_value=5, min_value=0)
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
