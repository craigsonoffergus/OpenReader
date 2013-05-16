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
        if not self.key:
            for _ in range(10):
                key = key_generator(7)
                if not type(self).objects.filter(key = key).count():
                    self.key = key
                    break
        super(Base, self).save()
        
    class Meta:
        abstract = True


class Feed(Base):
    url = models.CharField(max_length=256, blank = False, unique = True)
    name = models.CharField(max_length=256, blank = True)
    link = models.CharField(max_length=256, blank = True)
    description = models.CharField(max_length=256, blank = True)
    last_read = models.DateTimeField()
    regular_update_time = models.TimeField(null = True, blank = True)
    feed_last_modified = models.CharField(max_length=256, blank = True)
    feed_etag = models.CharField(max_length=256, blank = True)
    users = models.ManyToManyField(User, related_name="feeds")

    def __unicode__(self):
        return u"{0} ({1})".format(self.name, self.key)

class ReadFeedItem(models.Model):
    user = models.ForeignKey(User)
    feed_item = models.ForeignKey('FeedItem')

class FeedItem(Base):
    feed = models.ForeignKey(Feed, related_name="items")
    title = models.CharField(max_length=256)
    link = models.CharField(max_length=256)
    content = models.TextField()
    date = models.DateTimeField()
    author = models.CharField(max_length=64)
    remote_feed_id = models.CharField(max_length=256)
    read_by_users = models.ManyToManyField(User, through=ReadFeedItem, related_name="read_feed_items")
    
    def to_dict(self):
        return dict(title = self.title, 
                    link = self.link, 
                    content = self.content, 
                    author = self.author, 
                    date = self.date.isoformat(), 
                    feed = self.feed.key, 
                    feed_name = self.feed.name, 
                    key = self.key)
    
    def __unicode__(self):
        return u"{0} ({1})".format(self.title, self.key)
