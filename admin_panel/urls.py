from django.conf.urls import url
from . import views

urlpatterns = [

    # Admin landing page
    url('^$', views.main, name='main'),

    # Account management
    url('^sign_in/$', views.user_sign_in, name='sign_in'),
    url('^sign_in/submit/$', views.user_sign_in_submit, name='sign_in_submit'),
    url('^register/$', views.create_account, name='create_account'),
    url('^create_account/submit/$', views.create_account_submit, name='create_account_submit'),
    url('^edit_account/$', views.update_account, name='update_account'),
    url('^edit_account/submit/$', views.update_account_submit, name='edit_account_submit'),
    url('^logout/$', views.sign_out, name='sign_out'),

    # Data management
    url('^scrape/$', views.scrape_main, name='scrape_main'),
    url('^scrape/submit/$', views.perform_scrape, name='perform_scrape'),
    # url('^scrape_history/$', views.scrape_history_index, name='scrape_history_index'),
    # url('^view_scraped_documents/$', views.scraped_documents_index, name='scraped_documents_index'),
    url('^view_all_documents/$', views.documents_index, name='documents_index'),

    # Index management
    url('^index/$', views.index_management, name='index_management'),
    url('^index/build_solr_schema/$', views.build_solr_schema, name='build_solr_schema'),
    url('^index/clear_index/$', views.clear_index, name='clear_index'),
    url('^index/update_index/$', views.update_index, name='update_index'),
    url('^index/rebuild_index/$', views.rebuild_index, name='rebuild_index'),

]