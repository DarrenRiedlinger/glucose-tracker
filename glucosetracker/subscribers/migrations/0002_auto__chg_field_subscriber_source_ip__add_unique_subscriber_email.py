# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Subscriber.source_ip'
        db.alter_column(u'subscribers_subscriber', 'source_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True))
        # Adding unique constraint on 'Subscriber', fields ['email']
        db.create_unique(u'subscribers_subscriber', ['email'])


    def backwards(self, orm):
        # Removing unique constraint on 'Subscriber', fields ['email']
        db.delete_unique(u'subscribers_subscriber', ['email'])


        # Changing field 'Subscriber.source_ip'
        db.alter_column(u'subscribers_subscriber', 'source_ip', self.gf('django.db.models.fields.IPAddressField')(default=None, max_length=15))

    models = {
        u'subscribers.subscriber': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Subscriber'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'source_ip': ('django.db.models.fields.IPAddressField', [], {'default': 'None', 'max_length': '15', 'null': 'True'})
        }
    }

    complete_apps = ['subscribers']