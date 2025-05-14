from django.utils.timezone import now


def truncate_string(value, length):
    return value[:length] + '...' if len(value) > length else value


def filter_posts(queryset):
    return queryset.select_related('location', 'author', 'category').filter(
        pub_date__lte=now(),
        is_published=True,
        category__is_published=True,
    )
