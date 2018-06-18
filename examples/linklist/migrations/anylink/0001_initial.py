# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-18 12:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnyLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=150, verbose_name='text')),
                ('title', models.CharField(blank=True, max_length=150, verbose_name='title')),
                ('target', models.CharField(choices=[('_self', 'same window'), ('_blank', 'new window')], default='_self', max_length=7, verbose_name='target')),
                ('css_class', models.CharField(blank=True, max_length=255, verbose_name='css class')),
                ('link_type', models.CharField(choices=[('external_url', 'external url'), ('linkableobject', 'linkable object')], max_length=100, verbose_name='type')),
                ('external_url', models.URLField(blank=True, max_length=255, verbose_name='external url')),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
            },
        ),
    ]