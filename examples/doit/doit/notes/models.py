from django.db import models


class Note(models.Model):
    subject = models.CharField(max_length=254)
    comment = models.TextField()


class Item(models.Model):
    note = models.ForeignKey(Note)
    description = models.TextField()
