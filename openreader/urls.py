from django.conf.urls import patterns, url
from django_openid_auth import views as oauth_views
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

def default_render_failure(request, message, status=403,
                           template_name='',
                           exception=None):
    """Render an error page to the user."""
    return redirect(reverse("reader:login_failed"))

oauth_views.default_render_failure = default_render_failure

def login_begin(request):
    return oauth_views.login_begin(request, login_complete_view='reader:openid-complete')
    
urlpatterns = patterns('',
    url(r'^$', 'openreader.views.index', name='index'),
    url(r'^reader/', 'openreader.views.reader', name='reader'),
    url(r'^readercontent/', 'openreader.views.reader_content', name='reader_content'),
    url(r'^unreadcounts/', 'openreader.views.get_unread_counts', name='get_unread_counts'),
    url(r'^readitem/', 'openreader.views.read_item', name='read_item'),
    url(r'^addfeed/', 'openreader.views.add_feed', name='add_feed'),
    url(r'^removefeed/', 'openreader.views.remove_feed', name='remove_feed'),
    url(r'^completelogin/$', oauth_views.login_complete, name='openid-complete'),
    url(r'^loginfailed/$', TemplateView.as_view(template_name='loginfailure.html'), name="login_failed"),
    url(r'^login', login_begin, name='openid-login'),
    url(r'^logout', 'openreader.views.readerlogout', name='logout'),
)
