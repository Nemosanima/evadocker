from django.core.paginator import Paginator

NUMBER_OF_POSTS: int = 10


def page(queryset, request):
    paginator = Paginator(queryset, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
