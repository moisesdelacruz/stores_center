from django.conf.urls import url
from product import views

urlpatterns = [
    url(r'^$', views.ProductListView.as_view(), name='list'),
    url(r'^(?P<uuid>[\w-]+)/detail/$',
        views.ProductDetailView.as_view(), name='detail'),
    url(r'^shop/(?P<slug>[\w-]+)/new/$',
        views.ProductCreateView.as_view(), name='new'),
    url(r'^(?P<uuid>[\w-]+)/delete/$',
        views.ProductDeleteView.as_view(), name='delete'),
]
