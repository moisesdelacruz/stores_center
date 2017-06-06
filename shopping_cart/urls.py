from django.conf.urls import url
from shopping_cart import views

urlpatterns = [
    url(r'^add/$', views.CartProductView.as_view(), name='add'),
]
