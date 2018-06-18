# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-18 12:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('example_project', '0001_initial'),
        ('anylink', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='anylink',
            name='linkableobject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='example_project.LinkableObject', verbose_name='linkable object'),
        ),
    ]
