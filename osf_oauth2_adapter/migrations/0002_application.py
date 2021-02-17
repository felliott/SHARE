# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-09 15:34
from __future__ import unicode_literals

import os

from django.db import migrations


def create_socialapp(apps, schema_editor):
    Site = apps.get_model('sites', 'site')
    SocialApp = apps.get_model('socialaccount', 'socialapp')
    if not SocialApp.objects.exists():
        app = SocialApp.objects.using(schema_editor.connection.alias).create(
            key='',
            name='OSF',
            provider='osf',
            # Defaults are valid for staging
            client_id=os.environ.get('OSF_OAUTH_CLIENT_ID', 'b73fff80f83f4a5db8a60ff101718f03'),
            secret=os.environ.get('OSF_OAUTH_SECRET', 'AdaI80f8vFLJo2OqE9m8fefpARAfptD5134HJd4X'),
        )
        app.sites.add(Site.objects.get(domain='osf.io'))


def create_site(apps, schema_editor):
    Site = apps.get_model('sites', 'site')
    if not Site.objects.exists():
        Site.objects.db_manager(schema_editor.connection.alias).using(schema_editor.connection.alias).create(domain='osf.io', name='OSF')


class Migration(migrations.Migration):

    dependencies = [
        ('osf_oauth2_adapter', '0001_make_human_group'),
        ('share', '0001_initial_squashed_0020_auto_20170206_2114'),
        ('sites', '0002_alter_domain_unique'),
        ('socialaccount', '0003_extra_data_default_dict'),
    ]

    operations = [
        migrations.RunPython(create_site),
        migrations.RunPython(create_socialapp),
    ]
