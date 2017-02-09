from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'cz4034.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Default admin panel, provided by Django
    # url(r'^admin/', include(admin.site.urls)),

    # Customized admin panel
    url(r'^admin/', include('admin_panel.urls')),

    # User application
    url(r'^', include('user_app.urls')),
]
