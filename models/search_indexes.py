import datetime
from haystack import indexes
from models import *


class DocumentsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    hotel_name = indexes.CharField(model_attr='hotel_name')
    rating = indexes.CharField(model_attr='rating')

    def get_model(self):
        return Hotel_Review

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created_at__lte=datetime.datetime.now())
        # return self.get_model().objects.all()
