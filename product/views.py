# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# this project
from product.models import Product
from product.forms import ProductModelForm
from product.mixins import IsOwnerMixin
from shop.models import Shop

# Create your views here.

class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        for index, product in enumerate(self.object_list):
            if product.discount:
                self.object_list[index].new_price = (float(product.price)
                    - ((product.discount * float(product.price)) / 100))
        return context

class ProductDetailView(DetailView):
    model = Product
    pk_url_kwarg = 'uuid'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        if self.object.discount:
            self.object.new_price = (float(self.object.price)
                - ((self.object.discount * float(self.object.price)) / 100))
        return context

class ProductCreateView(LoginRequiredMixin, IsOwnerMixin, CreateView):
    model = Product
    form_class = ProductModelForm
    pk_url_kwarg = 'uuid'
    slug_or_pk_shop = 'shop_slug'

    def get_success_url(self):
        return reverse_lazy('product:detail', args=(self.object.pk,))

    def form_valid(self, form):
        form_serialized = form.save(commit=False)
        form_serialized.shop = self.shop
        form_serialized.save()
        return super(ProductCreateView, self).form_valid(form)

class ProductUpdateView(LoginRequiredMixin, IsOwnerMixin, UpdateView):
    model = Product
    form_class = ProductModelForm
    pk_url_kwarg = 'uuid'
    slug_or_pk_shop = 'shop_slug'

    def get_success_url(self):
        return reverse_lazy('product:detail', args=(self.object.pk,))

class ProductDeleteView(LoginRequiredMixin, IsOwnerMixin, DeleteView):
    model = Product
    pk_url_kwarg = 'uuid'
    slug_or_pk_shop = 'shop_slug'

    def get_success_url(self):
        return reverse_lazy('shop:detail', args=(self.object.shop.slug,))
