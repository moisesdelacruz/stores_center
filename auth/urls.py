from django.conf.urls import url
from auth import views

urlpatterns = [
    url(r'^signin/$', views.SigninView.as_view(), name='signin'),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
]
