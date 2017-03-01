from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ScrapeHistory(models.Model):
    """
    List of scraping history
    """
    def __str__(self):
        return self.id
    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=500, default="")
    keyword = models.CharField(max_length=200, default="")
    n_tweets = models.IntegerField(default=0)
    scraped_at = models.DateTimeField()

class Documents(models.Model):
    """
    List of documents
    """
    def __str__(self):
        return self.name
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, default="")
    screen_name = models.CharField(max_length=200, default="")
    status = models.CharField(max_length=1000, default="")
    location = models.CharField(max_length=200, null=True)
    source = models.CharField(max_length=500, null=True)
    scrape_history = models.ForeignKey(ScrapeHistory, null=False)
    created_at = models.DateTimeField()


