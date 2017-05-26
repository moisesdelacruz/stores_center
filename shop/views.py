# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from shop.models import Shop
from shop.forms import ShopModelForm

from product.models import Product
from product.mixins import IsOwnerMixin

# Create your views here.

class ShopDetailView(DetailView):
    model = Shop

    def get_context_data(self, **kwargs):
        context = super(ShopDetailView, self).get_context_data(**kwargs)
        self.product_list = Product.objects.filter(shop=self.object)
        for index, product in enumerate(self.product_list):
            if product.discount:
                self.product_list[index].new_price = (float(product.price)
                    - ((product.discount * float(product.price)) / 100))
        context['products'] = self.product_list
        return context

class ShopCreateView(LoginRequiredMixin, CreateView):
    model = Shop
    form_class = ShopModelForm

    def form_valid(self, form):
        __object = form.save(commit=False)
        __object.owner = self.request.user
        self.object = __object.save()
        return super(ShopCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('shop:detail', args=(self.object.slug,))


class ShopUpdateView(LoginRequiredMixin, IsOwnerMixin, UpdateView):
    model = Shop
    form_class = ShopModelForm

    def get_success_url(self):
        return reverse_lazy('shop:detail', args=(self.object.slug,))

class ShopDeleteView(LoginRequiredMixin, IsOwnerMixin, DeleteView):
    model = Shop

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.request.user.username,))
