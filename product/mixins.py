from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseNotFound, HttpResponseForbidden
from shop.models import Shop

class IsOwnerMixin(AccessMixin):
    slug_or_pk_shop = 'slug'

    def dispatch(self, request, *args, **kwargs):
        # if request.user is owner
        self.shop = get_object_or_404(Shop, slug=self.kwargs[self.slug_or_pk_shop])
        if not request.user == self.shop.owner:
            return HttpResponse('Not Fount', status=404)
        return super(IsOwnerMixin, self).dispatch(request, *args, **kwargs)
