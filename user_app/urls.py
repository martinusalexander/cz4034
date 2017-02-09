from django.conf.urls import include, url
from . import views


urlpatterns = [
    url('^$', views.main, name='main'),
    url('^about/$', views.about, name='about'),
    url('^search/$', views.search_documents, name='search_documents')

]