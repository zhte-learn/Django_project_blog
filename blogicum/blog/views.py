from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .constants import POST_LIMIT
from .models import Category, Post
from .forms import ProfileForm, PostForm

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


def profile_view(request, username):
    profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(
        author=profile,
        is_published=True
    )
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'profile': profile,
        'page_obj': page_obj,
    }
    return render(request, 'blog/profile.html', context)


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
