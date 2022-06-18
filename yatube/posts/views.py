from core.paginator import paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from posts.forms import CommentForm, PostForm
from posts.models import Follow, Comment, Post, Group, User
from django.views.decorators.cache import cache_page


LMT_PSTS: int = 10
CACHE_TIME: int = 20


@cache_page(CACHE_TIME)
def index(request):
    """View main page."""
    template = 'posts/index.html'
    posts = Post.objects.select_related('group')
    page_obj = paginator(request, posts)
    context = {
        'page_obj': page_obj,
        'is_index': True,
        'follow': False,
    }
    return render(request, template, context)


def group_posts(request, slug):
    """View group page."""
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.group_list.select_related('group')
    page_obj = paginator(request, posts)
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
    """View profile page."""
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related('author')
    page_obj = paginator(request, posts)
    following = (
        request.user.is_authenticated
        and Follow.objects.filter(user=request.user, author=author).exists()
    )
    context = {
        'author': author,
        'page_obj': page_obj,
        'posts': posts,
        'is_profile': True,
        'following': following
    }
    return render(request, template, context)


def post_detail(request, post_id):
    """View page selected post."""
    template = 'posts/post_detail.html'
    posts = get_object_or_404(Post, id=post_id)
    title = f'Пост: {posts.text[0:30]}'
    author = posts.author
    cnt = author.posts.count()
    form = CommentForm(request.POST or None)
    comment = Comment.objects.filter(post_id=post_id)
    comment_cnt = comment.count()
    subscribers = (
        Follow.objects.filter(author=author)
    )
    subscriptions = (
        Follow.objects.filter(user=author)
    )
    context = {
        'posts': posts,
        'title': title,
        'author': author,
        'cnt': cnt,
        'form': form,
        'comments': comment,
        'comment_cnt': comment_cnt,
        'subscribers': subscribers,
        'subscriptions': subscriptions
    }
    return render(request, template, context)


@login_required
def post_create(request):
    """View creating a post."""
    template = 'posts/create_post.html'
    form = PostForm(request.POST or None, files=request.FILES or None)
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
    """View post editing."""
    template = 'posts/create_post.html'
    required_post = Post.objects.get(id=post_id)
    if required_post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=required_post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'form': form,
        'required_post': required_post,
        'is_edit': True,
    }
    return render(request, template, context,)


@login_required
def add_comment(request, post_id):
    posts = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = posts
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    """Posts by selected authors."""
    template = 'posts/follow.html'
    post_list = Post.objects.filter(author__following__user=request.user)
    page_obj = paginator(request, post_list)
    context = {
        'page_obj': page_obj,
        'is_index': True,
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    """Subscribe to the author."""
    user = get_object_or_404(User, username=username)
    if request.user != user:
        Follow.objects.get_or_create(
            user_id=request.user.id,
            author_id=user.id
        )
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    """Unsubscribe from the author."""
    user = get_object_or_404(User, username=username)
    Follow.objects.filter(user_id=request.user.id, author_id=user.id).delete()
    return redirect('posts:profile', username=username)
