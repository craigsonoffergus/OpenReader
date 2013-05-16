from openreader.models import Feed
from openreader.feed_reader import read_feed

def read_all():
    for feed in Feed.objects.all():
        # TODO: you know, logic.
        read_feed(feed)

def read_some_feeds(feeds):
    for feed in feeds:
        # TODO: you know, the same logic.
        read_feed(feed)
        