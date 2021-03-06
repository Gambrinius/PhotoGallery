from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'registration/$', views.registration_view, name='registration'),
    url(r'login/$', views.login_view, name='login'),
    url(r'logout/$', views.logout_view, name='logout'),

    url(r'edit_profile/$', views.edit_view, name='edit_profile'),
    url(r'profile/(?P<user_id>[0-9]+)/$', views.profile_view, name='profile'),
    url(r'upload_image/$', views.upload_view, name='upload_image'),
    url(r'delete_image/$', views.delete_image_view, name='delete_image'),
]
