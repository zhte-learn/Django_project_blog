from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.timezone import now


from .constants import POST_LIMIT
from .models import Category, Post, Comment
from .forms import ProfileForm, PostForm, CommentForm

from .helpers import filter_posts, paginate_queryset


def index(request):
    posts = filter_posts(
        Post.objects.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')
    )

    page = paginate_queryset(
        posts,
        request.GET.get('page'),
        POST_LIMIT
    )
    return render(request, "blog/index.html", {"page_obj": page})


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related('author', 'location', 'category'),
        id=post_id
    )

    if (
        not post.is_published
        or not post.category.is_published
        or post.pub_date > now()
    ) and post.author != request.user:
        raise Http404("Пост недоступен")

    form = CommentForm()

    comments = post.comments.select_related('author').order_by('created_at')

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

    posts = filter_posts(
        category.posts.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')
    )

    page = paginate_queryset(
        posts,
        request.GET.get('page'),
        POST_LIMIT
    )

    return render(request, "blog/category.html", {
        "category": category,
        "page_obj": page,
    })


def profile_view(request, username):
    profile = get_object_or_404(User, username=username)

    posts = Post.objects.filter(
        author=profile
    ).annotate(comment_count=Count('comments'))

    if request.user != profile:
        posts = filter_posts(posts).order_by('-pub_date')

    page = paginate_queryset(
        posts.order_by('-pub_date'),
        request.GET.get('page'),
        POST_LIMIT
    )

    return render(request, 'blog/profile.html', {
        'profile': profile,
        'page_obj': page,
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'blog/user.html', {'form': form})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm()
    return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post.id)

    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return redirect('blog:post_detail', post_id=post.id)

    post.delete()
    return redirect('blog:index')


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'blog/comment.html', {'form': form, 'post': post})


@login_required
def edit_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        return redirect('blog:post_detail', post_id=post.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = CommentForm(instance=comment)

    return render(
        request,
        'blog/comment.html',
        {'form': form, 'post': post, 'comment': comment}
    )


@login_required
def delete_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        return redirect('blog:post_detail', post_id=post.id)

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post.id)

    return render(
        request,
        'blog/comment.html',
        {'comment': comment, 'post': post}
    )
