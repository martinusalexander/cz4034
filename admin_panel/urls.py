from django.conf.urls import url
from . import views


urlpatterns = [
    url('^$', views.main, name='main'),
    url('^sign_in/$', views.start_user_sign_in, name='start_sign_in'),
    url('^sign_in/submit/$', views.user_sign_in, name='sign_in'),
    url('^register/$', views.start_create_account, name='start_update_account'),
    url('^create_account/submit/$', views.create_account, name='create_account'),
    url('^edit_account/$', views.start_update_account, name='start_update_account'),
    url('^edit_account/submit/$', views.update_account, name='edit_account'),
    url('^logout/$', views.sign_out, name='sign_out')
]