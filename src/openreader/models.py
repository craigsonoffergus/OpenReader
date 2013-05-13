from django.db import models
from django.contrib.auth.models import User
import string
import random

def key_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Base(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=7, unique = True, blank = False)
    date_created = models.DateTimeField(auto_now_add = True)
    date_updated = models.DateTimeField(auto_now = True)
    
    
    def save(self):
        self.name = self.name.title()
        if not self.key:
            for _ in range(10):
                key = key_generator(7)
                if not type(self).objects.count(key == key):
                    self.key = key
                    break
        super(Base, self).save()
        
    class Meta:
        abstract = True


class Feed(Base):
    url = models.CharField(max_length=256, blank = False)
    name = models.CharField(max_length=256, blank = True)
    link = models.CharField(max_length=256, blank = True)
    description = models.CharField(max_length=256, blank = True)
    last_read = models.DateTimeField()
    regular_update_time = models.TimeField(null = True, blank = True)
    feed_last_modified = models.DateTimeField(null = True, blank = True)
    feed_etag = models.CharField(max_length=256, blank = True)
    users = models.ManyToManyField(User, related_name="feeds")

class FeedItemToUser(models.Model):
    is_read = models.BooleanField()
    user = models.ForeignKey(User)
    feed_item = models.ForeignKey('FeedItem')

class FeedItem(Base):
    feed = models.ForeignKey(Feed, related_name="items")
    title = models.CharField(max_length=256)
    link = models.CharField(max_length=256)
    content = models.TextField()
    date = models.DateTimeField()
    users = models.ManyToManyField(User, through=FeedItemToUser, related_name="feed_items")
