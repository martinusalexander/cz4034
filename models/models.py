from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

import datetime

# Create your models here.

REVIEW_TYPE = [
        ('Unknown', 'Unknown'),
        ('Location', 'Location'),
        ('Room', 'Room'),
        ('Facilities & Services', 'Facilities & Services'),
        ('General', 'General'),
    ]

LABELLING_METHOD = [
        ('Manual', 'Manual'),
        ('Automatic', 'Automatic'),
    ]

class Hotel(models.Model):
    """
    List of hotels
    """
    def __str__(self):
        return self.name
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, default="", null=False)
    star = models.FloatField(default=0, null=False)
    rating = models.FloatField(default=0, null=False)
    url = models.URLField(default="https://www.agoda.com", null=False)
    image_url = models.URLField(default="https://www.agoda.com", null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Hotel_Label(models.Model):
    """
    List of hotel label
    """
    def __str__(self):
        return self.label
    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=100, default="Unknown", choices=REVIEW_TYPE, null=False)
    method = models.CharField(max_length=100, default="Automatic", choices=LABELLING_METHOD, null=False)


class Hotel_Review(models.Model):
    """
    List of hotel review
    """
    def __str__(self):
        return self.title
    id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(Hotel, null=False)
    title = models.CharField(max_length=500, default="", null=False)
    content = models.CharField(max_length=2500, default="", null=False)
    rating = models.FloatField(default=0, null=False)
    date = models.DateField(null=True)
    label = models.OneToOneField(Hotel_Label, null=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

