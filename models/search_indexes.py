import datetime
from haystack import indexes
from models import Documents


class DocumentsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr='id')
    author = indexes.CharField(model_attr='name')
    screen_name = indexes.CharField(model_attr='screen_name')
    location = indexes.CharField(model_attr='location')
    source = indexes.CharField(model_attr='source')
    created_at = indexes.DateTimeField(model_attr='created_at')

    def get_model(self):
        return Documents

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        # return self.get_model().objects.filter(created_at__lte=datetime.datetime.now())
        return self.get_model().objects.all()
