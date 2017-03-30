from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

import datetime

# Create your models here.

HOTEL_TYPE = [
        ('Business', 'Business'),
        ('Recreation', 'Recreation'),
    ]

class Hotel(models.Model):
    """
    List of hotels
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, default="", null=False)
    star = models.IntegerField(default=0, null=False)
    rating = models.FloatField(default=0, null=False)
    url = models.URLField(default="https://www.agoda.com", null=False)
    image_url = models.URLField(default="https://www.agoda.com", null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Hotel_Label(models.Model):
    """
    List of hotel label
    """
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100, default="Recreation", choices=HOTEL_TYPE,   null=False)

class Hotel_Review(models.Model):
    """
    List of hotel review
    """
    def __str__(self):
        return self.name
    id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(Hotel, null=False)
    title = models.CharField(max_length=500, default="", null=False)
    content = models.CharField(max_length=2500, default="", null=False)
    rating = models.FloatField(default=0, null=False)
    date = models.DateField(null=True)
    label = models.OneToOneField(Hotel_Label, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
