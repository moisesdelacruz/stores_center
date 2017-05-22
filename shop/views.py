# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from shop.models import Shop
from shop.forms import ShopModelForm

from product.models import Product

# Create your views here.

class ShopDetailView(DetailView):
    model = Shop

    def get_context_data(self, **kwargs):
        context = super(ShopDetailView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.filter(shop=self.object)
        return context

class ShopCreateView(CreateView):
    model = Shop
    form_class = ShopModelForm
    # fields = ('name', 'description', 'logo', 'cover_image',)

    def form_valid(self, form):
        __object = form.save(commit=False)
        __object.owner = self.request.user
        self.object = __object.save()
        return super(ShopCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('shop:detail', args=(self.object.slug,))


class ShopUpdateView(UpdateView):
    model = Shop
    form_class = ShopModelForm

    def dispatch(self, request, *args, **kwargs):
        # if request.user is owner of the shop can edit
        self.shop = get_object_or_404(Shop, slug=self.kwargs['slug'])
        if not request.user == self.shop.owner:
            return HttpResponse('404')
        return super(ShopUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('shop:detail', args=(self.object.slug,))

class ShopDeleteView(DeleteView):
    model = Shop

    def dispatch(self, request, *args, **kwargs):
        # if request.user is owner of the shop can edit
        self.shop = get_object_or_404(Shop, slug=self.kwargs['slug'])
        if not request.user == self.shop.owner:
            return HttpResponse('404')
        return super(ShopDeleteView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.request.user.username,))
