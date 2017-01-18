from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'registration/$', views.registration_view, name='registration'),
    url(r'login/$', views.login_view, name='login'),
    url(r'logout/$', views.logout_view, name='logout'),
]
