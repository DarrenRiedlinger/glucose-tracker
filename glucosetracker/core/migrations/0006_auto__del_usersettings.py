# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'UserSettings'
        db.delete_table(u'core_usersettings')


    def backwards(self, orm):
        # Adding model 'UserSettings'
        db.create_table(u'core_usersettings', (
            ('glucose_low', self.gf('django.db.models.fields.PositiveIntegerField')(default=60)),
            ('glucose_target_max', self.gf('django.db.models.fields.PositiveIntegerField')(default=120)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='settings', unique=True, to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('time_zone', self.gf('django.db.models.fields.CharField')(default='America/New_York', max_length=155)),
            ('glucose_high', self.gf('django.db.models.fields.PositiveIntegerField')(default=180)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('glucose_target_min', self.gf('django.db.models.fields.PositiveIntegerField')(default=70)),
        ))
        db.send_create_signal(u'core', ['UserSettings'])


    models = {
        
    }

    complete_apps = ['core']