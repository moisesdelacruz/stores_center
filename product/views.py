# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
# this project
from product.models import Product
from shop.models import Shop

# Create your views here.

class ProductListView(ListView):
    model = Product

class ProductDetailView(DetailView):
    model = Product
    pk_url_kwarg = 'slug'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductModelForm

    def dispatch(self, request, *args, **kwargs):
        # if request.user is owner of the shop can publish
        self.shop = get_object_or_404(Shop, slug=self.kwargs['slug'])
        if not request.user == self.shop.user:
            return HttpResponse('404')
        return super(Product, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('product:detail', args=(self.object.pk,))

    def form_valid(self, form):
        form_serialized = form.save(commit=False)
        form_serialized.shop = self.shop
        form_serialized.save()
        return super(ProductCreateView, self).form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ('name', 'categories', 'description', 'photo',)

    def dispatch(self, request, *args, **kwargs):
        # if request.user is owner of the shop can update
        self.shop = get_object_or_404(Shop, slug=self.kwargs['slug'])
        if not request.user == self.shop.user:
            return HttpResponse('404')
        return super(ProductUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('product:detail', args=(self.object.pk,))
