# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from review.models import Review
from product.models import Product
from utils.uuid_validate import validate_uuid

# Create your views here.

def review(request):
    if request.is_ajax():
        if validate_uuid(request.POST.get('product[id]')):
            product = get_object_or_404(Product, id=request.POST.get('product[id]'))
            obj, created = Review.objects.update_or_create(
                user=request.user, product=product,
                defaults={'comment': request.POST.get('comment'),
                    'rating': request.POST.get('product[rating]')},
            )
            if created:
                return JsonResponse({'success': 'created'}, status=201)
            else:
                return JsonResponse({'success': 'updated'}, status=201)
        else:
            return JsonResponse({'error': 'uuid not valid'}, status=400)
    else:
        return JsonResponse({'error': 'Request has to be of ajax type'}, status=400)
