from django.utils.timezone import now
from django.core.paginator import Paginator


def truncate_string(value, length):
    return value[:length] + '...' if len(value) > length else value


def filter_posts(queryset):
    return queryset.select_related('location', 'author', 'category').filter(
        pub_date__lte=now(),
        is_published=True,
        category__is_published=True,
    )


def paginate_queryset(queryset, page_number, limit):
    paginator = Paginator(queryset, limit)
    return paginator.get_page(page_number)
