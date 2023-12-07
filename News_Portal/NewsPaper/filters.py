from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput
from .models import Post

class PostFilter(FilterSet):
    added_after = DateTimeFilter(field_name='date',  lookup_expr= 'gt', widget=DateTimeInput(format='%d %m %Y', attrs={'type':'datetime-local'}))
    class Meta:
        model = Post
        fields = {'title': ['iregex'],
                  'category': ['exact'],
                  }