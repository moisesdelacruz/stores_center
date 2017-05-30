from django.conf.urls import url

from review import views

urlpatterns = [
    url(r'^$', views.review, name='new'),
]
