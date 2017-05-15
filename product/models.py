# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.db import models
from shop.models import Shop
import uuid

# funcion para almacenamiento de imagenes
def content_file_name(instance, filename):
    return '/'.join(['products', str(instance), filename])

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=45)
    description = models.TextField(blank=True, max_length=140)
    slug = models.SlugField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
		if self.title:
			self.slug = slugify(self.title)
			super(Category, self).save(*args, **kwargs)
		else:
			super(Category, self).save(*args, **kwargs)

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop = models.ForeignKey(Shop)
    name = models.CharField(max_length=60)
    categories = models.ManyToManyField(Category)
    description = models.TextField()
    photo = models.ImageField(upload_to=content_file_name)
    slug = models.SlugField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
		if self.id:
			self.slug = slugify(self.name)
			super(Product, self).save(*args, **kwargs)
		else:
			super(Product, self).save(*args, **kwargs)

    def categories_text(self):
        return ', '.join([category.__str__() for category in self.categories.all()])

    def photo_url(self):
        return self.photo.url
