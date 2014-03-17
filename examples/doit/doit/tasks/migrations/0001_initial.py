# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField()),
                ('due_to', models.DateTimeField()),
                ('priority', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3')])),
                ('color', models.CharField(max_length=254, choices=[('red', 'Red'), ('blue', 'Blue'), ('green', 'Green')])),
                ('notes', models.ManyToManyField(to='notes.Note')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
