from django_filters import rest_framework as filter

from posts.models import Post


class PostFilter(filter.FilterSet):
    text = filter.CharFilter(
        field_name='text',
        lookup_expr='icontains'
    )
    author = filter.CharFilter(
        field_name='author__username',
        lookup_expr='icontains'
    )
    group = filter.CharFilter(
        field_name='group__title',
        lookup_expr='icontains'
    )

    class Meta:
        model = Post
        fields = ('text', 'author', 'group')
