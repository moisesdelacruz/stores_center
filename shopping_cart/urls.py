from django.conf.urls import url
from shopping_cart import views

urlpatterns = [
    url(r'^$', views.CartProductListView.as_view(), name='list'),
    url(r'^add/$', views.CartProductAddView.as_view(), name='add'),
    url(r'^remove/$', views.CartProductDeleteView.as_view(), name='remove'),
    url(r'^pay/$', views.PayProductsView.as_view(), name='pay'),
]
