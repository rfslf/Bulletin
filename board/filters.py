from django_filters import FilterSet, DateRangeFilter
from .models import Reply, Bulletin


class BulletinFilter(FilterSet):
    created = DateRangeFilter()

    def __init__(self, *args, **kwargs):
        super(BulletinFilter, self).__init__(*args, **kwargs)
        self.filters['bulletin'].queryset = Bulletin.objects.filter(author_id=kwargs['request'])

    class Meta:
        model = Reply
        fields = ('reply', 'created', 'bulletin')