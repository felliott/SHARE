# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-03-15 02:41
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import share.models.ingest
import share.models.jobs


def migrate_push_sources(apps, schema_editor):
    from django.core.files.base import ContentFile
    FaviconImage = apps.get_model('share', 'FaviconImage')
    ShareUser = apps.get_model('share', 'ShareUser')
    Source = apps.get_model('share', 'Source')
    SourceConfig = apps.get_model('share', 'SourceConfig')

    for user in ShareUser.objects.filter(is_trusted=True):
        source = Source(
            user=user,
            name=user.username,
            long_title=user.long_title or user.username,
            home_page=user.home_page,
        )
        source.save()
        try:
            icon = ContentFile(FaviconImage.objects.get(user_id=user.id).image)
            source.icon.save(source.name, icon)
        except FaviconImage.DoesNotExist:
            pass

        config = SourceConfig(
            label=user.username,
            source=source,
        )
        config.save()


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0001_initial_squashed_0020_auto_20170206_2114'),
    ]

    operations = [
        migrations.RenameModel(
            'RawData',
            'RawDatum',
        ),
        migrations.CreateModel(
            name='Harvester',
            managers=[
                ('objects', share.models.ingest.NaturalKeyManager('key')),
            ],
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.TextField(unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='HarvestLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.UUIDField(null=True)),
                ('status', models.IntegerField(choices=[(0, 'Enqueued'), (1, 'In Progress'), (2, 'Failed'), (3, 'Succeeded'), (4, 'Rescheduled'), (5, 'Defunct'), (6, 'Forced'), (7, 'Skipped')], db_index=True, default=0)),
                ('context', models.TextField(blank=True, default='')),
                ('completions', models.IntegerField(default=0)),
                ('date_started', models.DateTimeField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('share_version', models.TextField(default=share.models.jobs.get_share_version, editable=False)),
                ('source_config_version', models.PositiveIntegerField()),
                ('end_date', models.DateTimeField(db_index=True)),
                ('start_date', models.DateTimeField(db_index=True)),
                ('harvester_version', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            managers=[
                ('objects', share.models.ingest.NaturalKeyManager('name')),
            ],
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
                ('long_title', models.TextField(unique=True)),
                ('home_page', models.URLField(null=True)),
                ('icon', models.ImageField(null=True, storage=share.models.ingest.SourceIconStorage(), upload_to=share.models.ingest.icon_name)),
            ],
        ),
        migrations.CreateModel(
            name='SourceConfig',
            managers=[
                ('objects', share.models.ingest.NaturalKeyManager('label')),
            ],
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.TextField(unique=True)),
                ('version', models.PositiveIntegerField(default=1)),
                ('base_url', models.URLField(null=True)),
                ('earliest_date', models.DateField(null=True)),
                ('rate_limit_allowance', models.PositiveIntegerField(default=5)),
                ('rate_limit_period', models.PositiveIntegerField(default=1)),
                ('harvester_kwargs', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('transformer_kwargs', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('disabled', models.BooleanField(default=False)),
                ('harvester', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='share.Harvester')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='share.Source')),
            ],
        ),
        migrations.CreateModel(
            name='SourceIcon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.BinaryField()),
                ('source_name', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SourceUniqueIdentifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.TextField()),
                ('source_config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='share.SourceConfig')),
            ],
        ),
        migrations.CreateModel(
            name='Transformer',
            managers=[
                ('objects', share.models.ingest.NaturalKeyManager('key')),
            ],
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.TextField(unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='rawdatum',
            options={'verbose_name_plural': 'Raw Data'},
        ),
        migrations.RenameField(
            model_name='rawdatum',
            old_name='date_harvested',
            new_name='date_created',
        ),
        migrations.RenameField(
            model_name='rawdatum',
            old_name='date_seen',
            new_name='date_modified',
        ),
        migrations.RenameField(
            model_name='rawdatum',
            old_name='data',
            new_name='datum',
        ),
        migrations.AlterField(
            model_name='rawdatum',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.RemoveField(
            model_name='rawdatum',
            name='tasks',
        ),
        migrations.AddField(
            model_name='rawdatum',
            name='logs',
            field=models.ManyToManyField(related_name='raw_data', to='share.HarvestLog'),
        ),
        migrations.AddField(
            model_name='sourceconfig',
            name='transformer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='share.Transformer'),
        ),
        migrations.AddField(
            model_name='source',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='harvestlog',
            name='source_config',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='harvest_logs', to='share.SourceConfig'),
        ),
        migrations.AddField(
            model_name='rawdatum',
            name='suid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='share.SourceUniqueIdentifier'),
        ),
        migrations.AlterUniqueTogether(
            name='sourceuniqueidentifier',
            unique_together=set([('identifier', 'source_config')]),
        ),
        migrations.AlterUniqueTogether(
            name='harvestlog',
            unique_together=set([('source_config', 'start_date', 'end_date', 'harvester_version', 'source_config_version')]),
        ),
        migrations.RunPython(migrate_push_sources),
        migrations.RemoveField(
            model_name='shareuser',
            name='favicon',
        ),
        migrations.RemoveField(
            model_name='shareuser',
            name='home_page',
        ),
        migrations.RemoveField(
            model_name='shareuser',
            name='long_title',
        ),
        migrations.DeleteModel(
            name='FaviconImage',
        ),
    ]
