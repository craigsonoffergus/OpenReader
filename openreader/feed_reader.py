import requests, feedparser, datetime, traceback
from time import mktime
from openreader.models import FeedItem
from django.utils.timezone import utc
import re

'''
class NotModifiedHandler(urllib2.BaseHandler):
  
    def http_error_304(self, req, fp, code, message, headers):
        addinfourl = urllib2.addinfourl(fp, headers, req.get_full_url())
        addinfourl.code = code
        return addinfourl
'''

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
        response = requests.get(url, headers=headers)
         
        if response.status_code == 304:
            # not modified!
            return True
    
        
        feed.feed_etag = response.headers.get("ETag", "")
        feed.feed_last_modified = response.headers.get("Last-Modified", "")
        
        content = response.text
        parsed = feedparser.parse(content)
        
        feed.name = parsed['feed']['title']
        feed.description = parsed['feed']['subtitle'][:255]
        feed.link = parsed['feed']['link']
        feed.last_read = datetime.datetime.now().replace(tzinfo=utc)
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
                            title = entry.get('title',''),
                            link = link,
                            content = entry.get('summary',''),
                            author = entry.get('author', ''),
                            date =  date)
            item.save()
    except Exception:
        traceback.print_exc()
        return False
    return True