from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseBadRequest

import json

from openreader.forms import NewFeedForm
from openreader.models import Feed, FeedItem
from feed_reader import read_feed

reader_login_required = login_required(login_url='/reader/')


def ajax_required(f):
    """
    AJAX request required decorator
    use it in your views:

    @ajax_required
    def my_view(request):
        ....

    """    
    def wrap(request, *args, **kwargs):
            if not request.is_ajax():
                return HttpResponseBadRequest()
            return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap

def index(request):
    if (request.user.is_authenticated()):
        return redirect(reverse("reader:reader"))
    return render_to_response("index.html")

def default_render_failure(request, message, status=403,
                           template_name='',
                           exception=None):
    """Render an error page to the user."""
    return redirect("/loginfailed/")

@reader_login_required
def reader(request):
    return render_to_response("reader.html", context_instance = RequestContext(request, 
                                            dict(form = NewFeedForm(),
                                                 feeds = request.user.feeds.order_by("name").all())))

@reader_login_required
def reader_content(request):
    my_feeds = request.user.feeds.all()
    feeditems = FeedItem.objects.filter(feed__in = my_feeds).exclude(read_by_users__id = request.user.id).order_by("-date").all()
    feeditemslist = [item.to_dict() for item in feeditems]
    return HttpResponse(json.dumps(dict(feeditemslist = feeditemslist)))

@require_POST
@ajax_required
@reader_login_required
def add_feed(request):
    form = NewFeedForm(request.POST)
    if not form.is_valid():
        return HttpResponse(json.dumps(dict(message="Please enter a valid URL")))
    
    url = form.cleaned_data['url']
    feed = None
    try:
        feed = Feed.objects.get(url = url)
    except Feed.DoesNotExist:
        feed = Feed(url = url)

    if not read_feed(feed):
        return HttpResponse(json.dumps(dict(message="Please enter a valid URL")))
        
    request.user.feeds.add(feed)
    feedslist = render_to_string("feedslist.html", context_instance = RequestContext(request, 
                                            dict(feeds = request.user.feeds.order_by("name").all())))
    return HttpResponse(json.dumps(dict(message="", feedslist = feedslist)))


@require_POST
@ajax_required
@reader_login_required
def remove_feed(request):
    feed_key = request.POST['key']
    feed = Feed.objects.get(key = feed_key)
    request.user.feeds.remove(feed)
    
    feedslist = render_to_string("feedslist.html", context_instance = RequestContext(request, 
                                            dict(feeds = request.user.feeds.order_by("name").all())))
    return HttpResponse(json.dumps(dict(feedslist = feedslist)))
