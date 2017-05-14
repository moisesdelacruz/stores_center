# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from product.models import Product, Category

# Register your models here.

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'categories_text', 'shop', 'photo_url',)
    list_filter = ('categories', 'shop__name',)
    filter_horizontal = ('categories',)
    search_fields = ('name', 'categories', 'shop',)

    def photo_url(self, obj):
        url = obj.photo_url()
        tag = '<img src="%s" width="70"/>' % url
        return tag

    photo_url.allow_tags = True
    photo_url.admin_order_field = 'photo'
