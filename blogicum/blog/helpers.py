from django.utils.timezone import now
from django.core.paginator import Paginator
from django.db.models import Count


def truncate_string(value, length):
    return value[:length] + '...' if len(value) > length else value


def filter_posts(queryset):
    return queryset.filter(
        pub_date__lte=now(),
        is_published=True,
        category__is_published=True,
    )


def annotate_with_comments(queryset):
    return queryset.select_related(
        "location",
        "author",
        "category").annotate(
        comment_count=Count("comments")
    ).order_by("-pub_date")


def paginate_queryset(queryset, page_number, limit):
    paginator = Paginator(queryset, limit)
    return paginator.get_page(page_number)
