from django.contrib import admin
from openreader.models import Feed, FeedItem, ReadFeedItem
from django.template.defaultfilters import escape
from django.core.urlresolvers import reverse
from openreader.scripts.read_feeds import read_some_feeds, read_all

class FeedAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    save_on_top = True
    search_fields = ('key','name','url','link','description')
    list_display = ('key', 'name', 'url', 'link', 'last_read')
    readonly_fields = ('key', 'link', 'description', 'last_read', 'regular_update_time', 'feed_last_modified', 'feed_etag')
    actions = ['read_feeds', 'read_all_feeds']
    fieldsets = [
        (None,               {'fields': ['key', 'name', 'url', 'link', 'description']}),
        ('Polling Information', {'fields': ['last_read', 'regular_update_time', 'feed_last_modified', 'feed_etag'], 'classes': ['collapse']}),
        ('Users', {'fields': ['users'], 'classes': ['collapse']}),
    ]
    

    def read_feeds(self, request, queryset):
        read_all()
    read_feeds.short_description = "Read the feeds to see if they have any new items."
    
    def read_all_feeds(self, request, queryset):
        read_some_feeds(queryset)
    read_all_feeds.short_description = "Read all feeds. This ignores what you have selected and affects all feeds"

class FeedItemAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    save_on_top = True
    search_fields = ('key','title','feed__key','title','link')
    list_display = ('key', 'feed_link', 'title', 'link', 'date')
    readonly_fields = ('key',)
    fieldsets = [
        (None,               {'fields': ['key', 'feed', 'title', 'link', 'content', 'date', 'author', 'remote_feed_id']}),
    ]
    def feed_link(self, model):
        return u'<a href="{0}">{1}</a>'.format(reverse("admin:openreader_feed_change", args=(model.feed.id,)) , escape(model.feed))
    feed_link.allow_tags = True
    feed_link.short_description = "Feed" 
    feed_link.admin_order_field = 'feed'

class ReadFeedItemAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    save_on_top = True
    list_display = ('id', 'user_link', 'feeditem_link')
    search_fields = ('user', 'feed_item')
    fieldsets = [
        (None,               {'fields': ['user', 'feed_item']}),
    ]
    def user_link(self, model):
        return u'<a href="{0}">{1}</a>'.format(reverse("admin:auth_user_change", args=(model.user.id,)) , escape(model.user))
    user_link.allow_tags = True
    user_link.short_description = "User"
    user_link.admin_order_field = 'user'

    def feeditem_link(self, model):
        return u'<a href="{0}">{1}</a>'.format(reverse("admin:openreader_feeditem_change", args=(model.feed_item.id,)) , escape(model.feed_item))
    feeditem_link.allow_tags = True
    feeditem_link.short_description = "FeedItem" 
    feeditem_link.admin_order_field = 'feed_item'

admin.site.register(Feed, FeedAdmin)
admin.site.register(FeedItem, FeedItemAdmin)
admin.site.register(ReadFeedItem, ReadFeedItemAdmin)
