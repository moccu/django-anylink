# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=254)),
                ('comment', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.ForeignKey(to='doit.Note', to_field=u'id')),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField()),
                ('due_to', models.DateTimeField()),
                ('priority', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3')])),
                ('notes', models.ManyToManyField(to='doit.Note')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
