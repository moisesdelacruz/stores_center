# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, FormView

# this project
from users.forms import UserCreateForm
from auth.forms import AuthForm

# Create your views here.

# Sign up
class SignupView(FormView):
    extra_context = None
    form_class = UserCreateForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('product:list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return super(SignupView, self).dispatch(request, *args, **kwargs)
        return redirect(reverse_lazy('product:list'))

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return super(SignupView, self).form_valid(form)

# Login
class SigninView(FormView):
    form_class = AuthForm
    template_name = 'auth/signin.html'
    extra_context = None
    success_url = reverse_lazy('product:list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return super(SigninView, self).dispatch(request, *args, **kwargs)
        return redirect(reverse_lazy('product:list'))

    def form_valid(self, form):
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(self.request, user)
                # redirect
                url_next = self.request.GET.get('next')
                if url_next is not None:
					return redirect(url_next)
                else:
					return super(SigninView, self).form_valid(form)
            else:
                return HttpResponse("Inactive user.")
        else:
            return super(SigninView, self).form_valid(form)

# Logout
class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('/')
