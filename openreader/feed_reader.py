import requests, feedparser, datetime, traceback
from time import mktime
from openreader.models import FeedItem
from django.utils.timezone import utc
import re
import logging

def read_feed(feed):
    
    url = feed.url
    etag = feed.feed_etag
    last_modified = feed.feed_last_modified
    
    headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36'}
    
    if etag:
        headers["If-None-Match"] = etag
      
    if last_modified:
        headers["If-Modified-Since"] = last_modified
    
    try:
        logging.getLogger('django').error("Getting Feed: " + url)
        response = requests.get(url, headers=headers, timeout = 1)
        logging.getLogger('django').error("Feed Done")
        
        if response.status_code == 304:
            # not modified!
            return True
    
        
        feed.feed_etag = response.headers.get("ETag", "")
        feed.feed_last_modified = response.headers.get("Last-Modified", "")
        
        content = response.text
        parsed = feedparser.parse(content)
        
        feed.name = parsed['feed']['title'][:255]
        feed.description = parsed['feed']['subtitle'][:255]
        feed.link = parsed['feed']['link'][:255]
        feed.last_read = datetime.datetime.now().replace(tzinfo=utc)
        logging.getLogger('django').error(feed.name)
        feed.save()
        
        for entry in parsed['entries']:
            remote_id = entry.get('id') or entry.get('guid') or entry.get("link",'') or entry.get("published",'')
            if remote_id and FeedItem.objects.filter(feed = feed, remote_feed_id = remote_id).count():
                continue
            date = datetime.datetime.fromtimestamp(mktime(entry['published_parsed'])).replace(tzinfo=utc)
            link = entry.get('link','')
            if not re.match(r'http(s?)://', link) and re.match(r'http(s?)://', remote_id):
                link = remote_id
            item = FeedItem(feed = feed,
                            remote_feed_id = remote_id,
                            title = entry.get('title','')[:255],
                            link = link[:255],
                            content = entry.get('summary',''),
                            author = entry.get('author', ''),
                            date =  date)
            item.save()
    except Exception:
        logging.getLogger('django').error(traceback.format_exc())
        return False
    return True