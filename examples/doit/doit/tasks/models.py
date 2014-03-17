from django.db import models


class Task(models.Model):
    description = models.TextField()
    due_to = models.DateTimeField()
    priority = models.PositiveIntegerField(choices=(
        (1, '1'),
        (2, '2'),
        (3, '3'),
    ))
    color = models.CharField(max_length=254, choices=(
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
    ))

    notes = models.ManyToManyField('notes.Note')
