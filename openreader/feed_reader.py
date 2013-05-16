import urllib2, feedparser, datetime, traceback
from time import mktime
from openreader.models import FeedItem
from django.utils.timezone import utc

class NotModifiedHandler(urllib2.BaseHandler):
  
    def http_error_304(self, req, fp, code, message, headers):
        addinfourl = urllib2.addinfourl(fp, headers, req.get_full_url())
        addinfourl.code = code
        return addinfourl

def read_feed(feed):
    
    url = feed.url
    etag = feed.feed_etag
    last_modified = feed.feed_last_modified
    
    req = urllib2.Request(url)
    if etag:
        req.add_header("If-None-Match", etag)
      
    if last_modified:
        req.add_header("If-Modified-Since", last_modified)
 
    try:
        opener = urllib2.build_opener(NotModifiedHandler())
        opener.addheaders = [('User-agent', 'Mozilla/5.0')] # shhhh
        url_handle = opener.open(req)
         
        if hasattr(url_handle, 'code') and url_handle.code == 304:
            print "the web page has not been modified"
            return True
    
        headers = url_handle.info()
        feed.feed_etag = headers.getheader("ETag") or ""
        feed.feed_last_modified = headers.getheader("Last-Modified") or ""
        
        content = url_handle.read()
        parsed = feedparser.parse(content)
        
        feed.name = parsed['feed']['title']
        feed.description = parsed['feed']['subtitle']
        feed.link = parsed['feed']['link']
        feed.last_read = datetime.datetime.now().replace(tzinfo=utc)
        feed.save()
        
        for entry in parsed['entries']:
            remote_id = entry.get('id') or entry.get('guid') or entry.get("link",'') or entry.get("published",'')
            if remote_id and FeedItem.objects.filter(feed = feed, remote_feed_id = remote_id).count():
                continue
            date = datetime.datetime.fromtimestamp(mktime(entry['published_parsed'])).replace(tzinfo=utc)
            item = FeedItem(feed = feed,
                            remote_feed_id = remote_id,
                            title = entry.get('title',''),
                            link = entry.get('link',''),
                            content = entry.get('summary',''),
                            author = entry.get('author', ''),
                            date =  date)
            item.save()
    except urllib2.URLError:
        traceback.print_exc()
        return False
    except Exception:
        traceback.print_exc()
        return False
    return True