from django.conf.urls import url

from shop import views

urlpatterns = [
    url(r'^create/$', views.ShopCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', views.ShopDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', views.ShopUpdateView.as_view(), name='edit'),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.ShopDeleteView.as_view(), name='delete'),
]
