from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post, Group, User


LMT_PSTS: int = 10


def index(request):
    """view main page."""
    template = 'posts/index.html'
    posts = Post.objects.select_related('group')
    paginator = Paginator(posts, LMT_PSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'is_index': True,
    }
    return render(request, template, context)


def group_posts(request, slug):
    """view group page."""
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.group_list.select_related('group')
    paginator = Paginator(posts, LMT_PSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = posts.select_related('group')
    title = group.title
    context = {
        'group': group,
        'page_obj': page_obj,
        'title': title,
        'count': count,
    }
    return render(request, template, context)


def profile(request, username):
    """view profile page."""
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related('author')
    paginator = Paginator(posts, LMT_PSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'page_obj': page_obj,
        'posts': posts,
        'is_profile': True,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    """view page selected post."""
    template = 'posts/post_detail.html'
    posts = get_object_or_404(Post, id=post_id)
    title = f'Пост: {posts.text[0:30]}'
    author = posts.author
    cnt = author.posts.count()
    context = {
        'posts': posts,
        'title': title,
        'author': author,
        'cnt': cnt,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    """view creating a post."""
    template = 'posts/create_post.html'
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=request.user.username)
    context = {
        'form': form,
        'is_edit': False,
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    """view post editing."""
    template = 'posts/create_post.html'
    required_post = Post.objects.get(id=post_id)
    if required_post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(request.POST or None, instance=required_post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'form': form,
        'required_post': required_post,
        'is_edit': True,
    }
    return render(request, template, context,)
