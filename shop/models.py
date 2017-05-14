# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import uuid

# funcion para almacenamiento de imagenes
def content_file_name(instance, filename):
    return '/'.join(['shops', str(instance), filename])

# Create your models here.
class Shop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=60)
    description = models.TextField()
    logo = models.ImageField(blank=True, upload_to=content_file_name)
    cover_image = models.ImageField(blank=True, upload_to=content_file_name)
    slug = models.SlugField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def logo_img(self):
        return self.logo.url

    def save(self, *args, **kwargs):
		if self.id:
			self.slug = slugify(self.name)
			super(Shop, self).save(*args, **kwargs)
		else:
			super(Shop, self).save(*args, **kwargs)
