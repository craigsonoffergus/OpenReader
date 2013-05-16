from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.views import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Count
import json

from openreader.forms import NewFeedForm
from openreader.models import Feed, FeedItem, ReadFeedItem
from openreader.feed_reader import read_feed


def reader_login_required(f):
    def wrap(request, *args, **kwargs):
        return login_required(login_url=reverse("reader:openid-login"))(f)(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap


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
    return render_to_response("openreader/index.html")

def readerlogout(request):
    return auth_logout(request, next_page = reverse('reader:index'))

@reader_login_required
def reader(request):
    feeds = request.user.feeds.order_by("name").all()
    return render_to_response("openreader/reader.html", context_instance = RequestContext(request, 
                                            dict(form = NewFeedForm(),
                                                 feeds = feeds)))

@ajax_required
@reader_login_required
def reader_content(request):
    query = None
    if request.GET.get("feed_key"):
        query = FeedItem.objects.filter(feed__key = request.GET.get("feed_key"))
    else:
        my_feeds = request.user.feeds.all()
        query = FeedItem.objects.filter(feed__in = my_feeds)
    
    feeditems = query.exclude(read_by_users__id = request.user.id).order_by("date").select_related('feed').all()
    feeditemslist = [item.to_dict() for item in feeditems]
    return HttpResponse(json.dumps(dict(feeditemslist = feeditemslist)))

@ajax_required
@reader_login_required
def get_unread_counts(request):
    my_feeds = request.user.feeds.all()
    feeditems = FeedItem.objects.filter(feed__in = my_feeds).exclude(read_by_users__id = request.user.id).values('feed__key').annotate(Count('feed__key')).values_list('feed__key','feed__key__count')
    feeditems_dict = dict(feeditems)
    feeditems_dict["totalunread"] = sum(feeditems_dict.values())
    return HttpResponse(json.dumps(dict(feeditemcounts = feeditems_dict)))

@require_POST
@ajax_required
@reader_login_required
def read_item(request):
    item_key = request.POST.get("item_key")
    item = FeedItem.objects.get(key = item_key)
    read_tag = ReadFeedItem(user = request.user, feed_item = item)
    read_tag.save()
    return HttpResponse("")

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
    
    old_feed_items = FeedItem.objects.filter(feed = feed).all()[10:]
    read_flags = []
    for item in old_feed_items:
        read_flags.append(ReadFeedItem(user = request.user, feed_item = item))
    ReadFeedItem.objects.bulk_create(read_flags)
    
    feedslist = render_to_string("openreader/feedslist.html", context_instance = RequestContext(request, 
                                            dict(feeds = request.user.feeds.order_by("name").all())))
    return HttpResponse(json.dumps(dict(message="", feedslist = feedslist, feedkey = feed.key)))


@require_POST
@ajax_required
@reader_login_required
def remove_feed(request):
    feed_key = request.POST['key']
    feed = Feed.objects.get(key = feed_key)
    request.user.feeds.remove(feed)
    ReadFeedItem.objects.filter(user_id = request.user.id, feed_item__feed = feed).delete()
    
    feedslist = render_to_string("openreader/feedslist.html", context_instance = RequestContext(request, 
                                            dict(feeds = request.user.feeds.order_by("name").all())))
    return HttpResponse(json.dumps(dict(feedslist = feedslist)))
