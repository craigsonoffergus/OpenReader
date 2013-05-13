# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feed'
        db.create_table(u'openreader_feed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=7)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('last_read', self.gf('django.db.models.fields.DateTimeField')()),
            ('regular_update_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('feed_last_modified', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('feed_etag', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
        ))
        db.send_create_signal(u'openreader', ['Feed'])

        # Adding M2M table for field users on 'Feed'
        db.create_table(u'openreader_feed_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feed', models.ForeignKey(orm[u'openreader.feed'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(u'openreader_feed_users', ['feed_id', 'user_id'])

        # Adding model 'ReadFeedItem'
        db.create_table(u'openreader_readfeeditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('feed_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openreader.FeedItem'])),
        ))
        db.send_create_signal(u'openreader', ['ReadFeedItem'])

        # Adding model 'FeedItem'
        db.create_table(u'openreader_feeditem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=7)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['openreader.Feed'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('remote_feed_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'openreader', ['FeedItem'])


    def backwards(self, orm):
        # Deleting model 'Feed'
        db.delete_table(u'openreader_feed')

        # Removing M2M table for field users on 'Feed'
        db.delete_table('openreader_feed_users')

        # Deleting model 'ReadFeedItem'
        db.delete_table(u'openreader_readfeeditem')

        # Deleting model 'FeedItem'
        db.delete_table(u'openreader_feeditem')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'openreader.feed': {
            'Meta': {'object_name': 'Feed'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'feed_etag': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'feed_last_modified': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '7'}),
            'last_read': ('django.db.models.fields.DateTimeField', [], {}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'regular_update_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'feeds'", 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        },
        u'openreader.feeditem': {
            'Meta': {'object_name': 'FeedItem'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['openreader.Feed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '7'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'read_by_users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'read_feed_items'", 'symmetrical': 'False', 'through': u"orm['openreader.ReadFeedItem']", 'to': u"orm['auth.User']"}),
            'remote_feed_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'openreader.readfeeditem': {
            'Meta': {'object_name': 'ReadFeedItem'},
            'feed_item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['openreader.FeedItem']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['openreader']