# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView

from shopping_cart.models import CartProduct
from product.models import Product

from utils.uuid_validate import validate_uuid

# Create your views here.

def validate_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

class CartProductListView(LoginRequiredMixin, ListView):
    model = CartProduct

    def get_queryset(self):
        return CartProduct.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(CartProductListView, self).get_context_data(**kwargs)
        for index, item in enumerate(self.object_list):
            # add discount to products
            if item.product.discount:
                self.object_list[index].product.new_price = (float(item.product.price)
                    - ((item.product.discount * float(item.product.price)) / 100))
        return context

class CartProductAddView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if (validate_uuid(request.POST.get('product'))
                and validate_int(request.POST.get('quantity'))):
                product = get_object_or_404(
                    Product, id=request.POST.get('product'))
                obj, created = CartProduct.objects.get_or_create(
                    user=request.user,
                    product=product,
                    quantity=int(request.POST.get('quantity'))
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
                if validate_uuid(request.POST.get('product')):
                    product = CartProduct.objects.get(
                        product=request.POST.get('product'), user=request.user)
                    product.delete()
                    return JsonResponse(
                        {'success': True}, status=200)
                else:
                    JsonResponse({'error': 'product id not valid'}, status=400)
            except CartProduct.DoesNotExist:
                return JsonResponse(
                    {'error': 'product not exist in your collection'}, status=404)
