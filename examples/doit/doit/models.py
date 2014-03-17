from django.core.urlresolvers import reverse
from django.db import models

from anylink.fields import AnyLinkField


class Note(models.Model):
    subject = models.CharField(max_length=254)
    comment = models.TextField()

    def get_absolute_url(self):
        return reverse('admin:doit_note_change', args=(self.pk,))


class Item(models.Model):
    note = models.ForeignKey(Note, null=True, blank=True)
    description = models.CharField(max_length=512)

    def get_absolute_url(self):
        return reverse('admin:doit_item_change', args=(self.pk,))


class Task(models.Model):
    description = models.TextField()
    due_to = models.DateTimeField()
    priority = models.PositiveIntegerField(choices=(
        (1, '1'),
        (2, '2'),
        (3, '3'),
    ))

    notes = models.ManyToManyField(Note)

    def get_absolute_url(self):
        return reverse('admin:doit_task_change', args=(self.pk,))
