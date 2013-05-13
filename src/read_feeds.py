from openreader import settings
from django.core.management import setup_environ
setup_environ(settings)

from openreader.models import Feed
from feed_reader import read_feed

for feed in Feed.objects.all():
    # TODO: you know, logic.
    read_feed(feed)
