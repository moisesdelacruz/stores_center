# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from shop.models import Shop

# Register your models here.

@admin.register(Shop)
class ShopModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'user', 'logo_img',)
    search_fields = ('name', 'user__username',)

    def logo_img(self, obj):
		url = obj.logo_img()
		tag = '<img src="%s" width="50"/>' % url
		return tag

    logo_img.allow_tags = True
    logo_img.admin_order_field = 'logo'
