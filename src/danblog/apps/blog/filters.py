import django_filters
from .models import Post

class PostFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    created = django_filters.DateFilter(lookup_expr='icontains')
    class Meta:
        model = Post
        fields = ['name', 'category', 'user', 'created']