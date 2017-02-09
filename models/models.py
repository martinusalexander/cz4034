from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Documents(models.Model):
    """
    List of documents (temporary only)
    """
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200, unique=True)
    content = models.TextField(max_length=1000)
    date = models.DateTimeField()