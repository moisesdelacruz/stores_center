# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from shopping_cart.models import CartProduct
from product.models import Product

from utils.uuid_validate import validate_uuid

# Create your views here.

class CartProductAddView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if validate_uuid(request.POST.get('product')):
                product = get_object_or_404(
                    Product, id=request.POST.get('product'))
                obj, created = CartProduct.objects.get_or_create(
                    user=request.user,
                    product=product
                )
                object = ({
                    'product': {
                        'id': str(obj.product.id),
                        'name': obj.product.name,
                        'photo': obj.product.photo.url
                    },
                    'user': {
                        'id': obj.user.id,
                        'username': obj.user.username
                    }
                })
                return JsonResponse(
                    {'object': object, 'created': created}, status=201)
            else:
                return JsonResponse({'error': 'uuid not is valid'}, status=400)
        else:
            return JsonResponse(
                {'error': 'request mush be of ajax type'}, status=400)


class CartProductDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                product = CartProduct.objects.get(
                    pk=request.POST.get('product[id]'), user=request.user)
                product.objects.delete()
            except CartProduct.DoesNotExist:
                return JsonResponse(
                    {'error': 'product not exist in collection'}, status=404)
