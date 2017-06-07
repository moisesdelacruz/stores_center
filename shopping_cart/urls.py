from django.conf.urls import url
from shopping_cart import views

urlpatterns = [
    url(r'^add/$', views.CartProductAddView.as_view(), name='add'),
    url(r'^remove/$', views.CartProductDeleteView.as_view(), name='remove'),
]
