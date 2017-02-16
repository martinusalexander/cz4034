from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Documents(models.Model):
    """
    List of documents
    """
    def __str__(self):
        return self.name
    id = models.BigIntegerField(name='id', primary_key=True)
    name = models.CharField(max_length=200, default="")
    screen_name = models.CharField(max_length=200, default="")
    status = models.CharField(max_length=1000, default="")
    location = models.CharField(max_length=200, null=True)
    source = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField()