from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^@(?P<slug>[\w-]+)/$', views.ProfileDetailView.as_view(), name='profile'),
]
