from django.db import models


class Note(models.Model):
    subject = models.CharField(max_length=254)
    comment = models.TextField()


class Item(models.Model):
    note = models.ForeignKey(Note)
    description = models.TextField()


class Task(models.Model):
    description = models.TextField()
    due_to = models.DateTimeField()
    priority = models.PositiveIntegerField(choices=(
        (1, '1'),
        (2, '2'),
        (3, '3'),
    ))

    notes = models.ManyToManyField(Note)
