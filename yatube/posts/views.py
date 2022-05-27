from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post, Group, User


LMT_PSTS: int = 10  # limit posts per page


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.select_related('group').all()
    paginator = Paginator(posts, LMT_PSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = 'Главная страница YaTube'
    text = 'Последние обновления на сайте'
    context = {
        'page_obj': page_obj,
        'title': title,
        'text': text,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.group_list.all()
    paginator = Paginator(posts, LMT_PSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = f'Группа {group.title}'
    context = {
        'group': group,
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related('author')
    paginator = Paginator(posts, LMT_PSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = 'профайл пользователя'
    context = {
        'title': title,
        'author': author,
        'page_obj': page_obj,
        'posts': posts,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    posts = get_object_or_404(Post, id=post_id)
    title = f'Пост {posts.text[0:31]}'
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
    is_edit = False
    template = 'posts/create_post.html'
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', request.user.username)
    context = {
        'form': form,
        'is_edit': is_edit,
    }
    return render(request, template, context)
