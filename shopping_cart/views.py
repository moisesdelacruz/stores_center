# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView

from shopping_cart.models import CartProduct
from product.models import Product
from users.models import User

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


class PayProductsView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        self.request = request
        if request.is_ajax():
            if request.POST.get('product') == 'all':
                items = CartProduct.objects.filter(user=request.user)
                # array donde se almacenaran los id de los products vendidos
                sold = []
                user_money = request.user.money
                # itera sobre los products
                for item in items:
                    # sumar el precio de todos los productos
                    price = self.cal_price(item.product, item.quantity)
                    # verificar que el usuario tenga suficiente dinero
                    if price <= float(request.user.money):
                        # cobrar al usuario
                        user_money = self.buyer_charge(price)
                        # pagar al owner del producto
                        self.pay_owner(item.product.shop.owner, price)
                        # add to the collection
                        sold.append(item.product.id)
                        # delete products from shopping cart
                        item.delete()
                return JsonResponse(
                    {'success': True, 'user_money': ("%.2f" % user_money), 'sold': sold},
                    status=200)
            else:
                try:
                    if validate_uuid(request.POST.get('product')):
                        item = CartProduct.objects.get(
                            product=request.POST.get('product'), user=request.user)
                        # sumar el precio de todos los productos
                        price = self.cal_price(item.product, item.quantity)
                        # verificar que el usuario tenga suficiente dinero
                        if price <= float(request.user.money):
                            # cobrar al usuario
                            user_money = self.buyer_charge(price)
                            # pagar al owner del producto
                            self.pay_owner(item.product.shop.owner, price)
                            # delete products from shopping cart
                            item.delete()
                            return JsonResponse(
                                {'success': True, 'user_money': ("%.2f" % user_money), 'sold': [item.product.id]},
                                status=200)
                        else:
                            return JsonResponse(
                                {'success': False, 'total_pay': ("%.2f" % price)},
                                status=204)
                    else:
                        JsonResponse({'error': 'product id not valid'}, status=400)
                except CartProduct.DoesNotExist:
                    return JsonResponse(
                        {'error': 'product not exist in your collection'}, status=404)

    def cal_price(self, product, quantity):
        price = float(product.price)
        # aplicar descuento
        if product.discount:
            price = (float(product.price)
                - ((product.discount
                * float(product.price))
                / 100))
        return price*float(quantity)

    def pay_owner(self, owner, money):
        owner = User.objects.get(pk=owner.pk)
        owner.money = float(owner.money) + money
        owner.save()

    def buyer_charge(self, money):
        user = User.objects.get(pk=self.request.user.pk)
        user.money = float(user.money)-money
        user.save()
        return user.money
