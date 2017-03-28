from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

import datetime

# Create your models here.

class Hotel_Review(models.Model):
    """
    List of documents
    """
    def __str__(self):
        return self.name
    id = models.AutoField(primary_key=True)
    hotel_name = models.CharField(max_length=500, default="", null=False)
    rating = models.FloatField(default=0, null=False)
    title = models.CharField(max_length=500, default="", null=False)
    content = models.CharField(max_length=2500, default="", null=False)
    date = models.DateField(null=True)
    url = models.URLField(default="https://www.agoda.com", null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)