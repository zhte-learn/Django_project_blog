from django.shortcuts import get_object_or_404, render

from .constants import POST_LIMIT
from .models import Category, Post
from .helpers import filter_posts


def index(request):
    post_list = filter_posts(Post.objects)[:POST_LIMIT]
    return render(request, "blog/index.html", {"post_list": post_list})


def post_detail(request, post_id):
    post = get_object_or_404(
        filter_posts(Post.objects),
        id=post_id,
    )
    return render(request, "blog/detail.html", {"post": post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    post_list = filter_posts(category.posts.all())

    return render(request, "blog/category.html", {
        "category": category,
        "post_list": post_list,
    })
