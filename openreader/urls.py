from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', 'openreader.views.index', name='index'),
    url(r'^reader/', 'openreader.views.reader', name='reader'),
    url(r'^readercontent/', 'openreader.views.reader_content', name='reader_content'),
    url(r'^unreadcounts/', 'openreader.views.get_unread_counts', name='get_unread_counts'),
    url(r'^readitem/', 'openreader.views.read_item', name='read_item'),
    url(r'^addfeed/', 'openreader.views.add_feed', name='add_feed'),
    url(r'^removefeed/', 'openreader.views.remove_feed', name='remove_feed'),
    url(r'^loginfailed/$', TemplateView.as_view(template_name='loginfailure.html'), name="login_failed"),
    url(r'^logout', 'openreader.views.readerlogout', name='logout'),
)
