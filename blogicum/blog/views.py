from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .constants import POST_LIMIT
from .models import Category, Post, Comment
from .forms import ProfileForm, PostForm, CommentForm
from .helpers import (
    filter_posts,
    paginate_queryset,
    annotate_with_comments
)


def index(request):
    posts = annotate_with_comments(filter_posts(Post.objects))

    page = paginate_queryset(
        posts,
        request.GET.get("page"),
        POST_LIMIT
    )
    return render(request, "blog/index.html", {"page_obj": page})


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related("author", "location", "category"),
        id=post_id
    )

    if post.author != request.user:
        post = get_object_or_404(
            filter_posts(
                Post.objects.select_related("author", "location", "category")
            ),
            id=post_id
        )

    form = CommentForm()

    comments = post.comments.select_related("author")

    return render(request, "blog/detail.html", {
        "post": post,
        "form": form,
        "comments": comments,
    })


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    posts = annotate_with_comments(
        filter_posts(category.posts.all())
    )

    page = paginate_queryset(
        posts,
        request.GET.get("page"),
        POST_LIMIT
    )

    return render(request, "blog/category.html", {
        "category": category,
        "page_obj": page,
    })


def profile_view(request, username):
    profile = get_object_or_404(User, username=username)

    if request.user == profile:
        posts = annotate_with_comments(
            profile.posts.select_related(
                "category",
                "location",
                "author"
            ).all()
        )
    else:
        posts = annotate_with_comments(
            filter_posts(profile.posts.all())
        )

    page = paginate_queryset(
        posts,
        request.GET.get("page"),
        POST_LIMIT
    )

    return render(request, "blog/profile.html", {
        "profile": profile,
        "page_obj": page,
    })


@login_required
def edit_profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)

    if form.is_valid():
        form.save()
        return redirect("blog:profile", username=request.user.username)

    return render(request, "blog/user.html", {"form": form})


@login_required
def create_post(request):
    form = PostForm(request.POST or None, files=request.FILES)

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("blog:profile", username=request.user.username)

    return render(request, "blog/create.html", {"form": form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not request.user.is_authenticated or post.author != request.user:
        return redirect("blog:post_detail", post_id=post.id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )

    if form.is_valid():
        form.save()
        return redirect("blog:post_detail", post_id=post.id)
    return render(request, "blog/create.html", {"form": form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return redirect("blog:post_detail", post_id=post.id)

    # Я не могу сделать проверку на POST, потому что в
    # шаблоне удаление происходит по ссылке GET.
    # Если меняю шаблон, но pytest выдает много ошибок.
    post.delete()
    return redirect("blog:profile", username=post.author.username)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return redirect("blog:post_detail", post_id=post.id)

    return render(request, "blog/comment.html", {"form": form, "post": post})


@login_required
def edit_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        return redirect("blog:post_detail", post_id=post.id)

    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect("blog:post_detail", post_id=post.id)

    return render(
        request,
        "blog/comment.html",
        {"form": form, "post": post, "comment": comment}
    )


@login_required
def delete_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        return redirect("blog:post_detail", post_id=post.id)

    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", post_id=post.id)

    return render(
        request,
        "blog/comment.html",
        {"comment": comment, "post": post}
    )
