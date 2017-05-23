from django.conf.urls import url
from product import views

urlpatterns = [
    url(r'^$', views.ProductListView.as_view(), name='list'),
    url(r'^(?P<uuid>[\w-]+)/detail/$',
        views.ProductDetailView.as_view(), name='detail'),
    url(r'^(?P<shop_slug>[\w-]+)/new/$',
        views.ProductCreateView.as_view(), name='new'),
    url(r'^(?P<shop_slug>[\w-]+)/(?P<uuid>[\w-]+)/edit/$',
        views.ProductUpdateView.as_view(), name='edit'),
    url(r'^(?P<shop_slug>[\w-]+)/(?P<uuid>[\w-]+)/delete/$',
        views.ProductDeleteView.as_view(), name='delete'),
]
