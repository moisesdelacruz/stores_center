from django.conf.urls import url

from review import views

urlpatterns = [
    url(r'^$', views.ReviewView.as_view(), name='new'),
]
