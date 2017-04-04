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
    url('^index/clear_index/$', views.clear_index, name='clear_index'),
    url('^index/update_index/$', views.update_index, name='update_index'),
    url('^index/rebuild_index/$', views.rebuild_index, name='rebuild_index'),

    # Labelling
    url('^labelling/$', views.labelling, name='labelling'),
    url('^labelling/change_label/$', views.change_label, name='change_label'),

    # Classification
    url('^classification/$', views.classification_management, name='classification_management'),
    url('^classification/visualise$', views.classification_visualise, name='classification_visualise'),
    url('^classification/classify', views.classification_classify, name='classification_classify'),
    url('^classification/import_data/$', views.classification_import_data, name='import_data'),
    url('^classification/preprocess/$', views.classification_preprocess, name='preprocess'),
    url('^classification/train/$', views.classification_train, name='train'),

]
