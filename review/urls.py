from django.conf.urls import url

from review import views

urlpatterns = [
    url(r'^(?P<product>[-\ \w]+)/new/$',
        views.ReviewCreateView.as_view(), name='new'),
]
