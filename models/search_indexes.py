import datetime
from haystack import indexes
from models import *
import re


class DocumentsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    hotel_name = indexes.CharField(model_attr='hotel__name')
    hotel_star = indexes.FloatField(model_attr='hotel__star')
    hotel_rating = indexes.FloatField(model_attr='hotel__rating')
    review_title = indexes.CharField(model_attr='title')
    review_content = indexes.CharField(model_attr='content')
    review_rating = indexes.FloatField(model_attr='rating')
    date = indexes.DateField(model_attr='date', indexed=False)
    label = indexes.CharField(model_attr='label__label')
    hotel_url = indexes.CharField(model_attr='hotel__url', indexed=False)
    image_url = indexes.CharField(model_attr='hotel__image_url', indexed=False)

    def get_model(self):
        return Hotel_Review

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created_at__lte=datetime.datetime.now())
        # return self.get_model().objects.all()
