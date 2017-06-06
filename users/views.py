# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from users.models import User

from shop.models import Shop

# Create your views here.

class ProfileDetailView(DetailView):
    model = User
    template_name = 'users/user_detail.html'

    def get_object(self):
        # original qs
        qs = super(ProfileDetailView, self).get_queryset()
        # filter by a variable captured from url, for example
        return qs.filter(username=self.kwargs['slug']).first()

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['shops'] = Shop.objects.filter(owner=self.object)
        return context
