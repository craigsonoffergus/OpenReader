from django.conf.urls import patterns, include, url
from django_openid_auth import views as oauth_views
from openreader.views import default_render_failure
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponseRedirect

admin.autodiscover()

oauth_views.default_render_failure = default_render_failure

readerpatterns = patterns('',
    url(r'^$', 'openreader.views.index', name='index'),
    url(r'^reader/', 'openreader.views.reader', name='reader'),
    url(r'^readercontent/', 'openreader.views.reader_content', name='reader_content'),
)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^reader/', include(readerpatterns, 'reader/', 'reader')),
    
    url(r'^completelogin/$', oauth_views.login_complete, name='openid-complete'),
    url(r'^loginfailed/$', TemplateView.as_view(template_name='loginfailure.html')),
    url(r'^login', oauth_views.login_begin, name='openid-login'),
    url(r'^logout', 'django.contrib.auth.views.logout', {'next_page': '/reader/',}, name='logout'),
    url(r'^',  lambda x: HttpResponseRedirect('/reader/')),
)


urlpatterns += staticfiles_urlpatterns()
