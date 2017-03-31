import datetime
from haystack import indexes
from models import *


class DocumentsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    hotel_name = indexes.CharField(model_attr='hotel__name')
    hotel_star = indexes.CharField(model_attr='hotel__star')
    hotel_rating = indexes.CharField(model_attr='hotel__rating')
    review_title = indexes.CharField(model_attr='title')
    review_content = indexes.CharField(model_attr='content')
    review_rating = indexes.CharField(model_attr='rating')
    date = indexes.CharField(model_attr='date')
    label = indexes.CharField(model_attr='label__type')

    def get_model(self):
        return Hotel_Review

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created_at__lte=datetime.datetime.now())
        # return self.get_model().objects.all()
