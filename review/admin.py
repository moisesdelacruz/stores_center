# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from review.models import Review

# Register your models here.


@admin.register(Review)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'comment',)
