from django.shortcuts import render, get_object_or_404

from .models import Post, Group

LMT_PSTS = 10  # limit posts per page


def index(request):
    posts = Post.objects.all()[:LMT_PSTS]
    title = 'Главная страница YaTube'
    text = 'Последние обновления на сайте'
    context = {
        'title': title,
        'text': text,
        'posts': posts
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.group_list.all()[:LMT_PSTS]
    title = f'Записи сообщества {group.title}'
    context = {
        'group': group,
        'posts': posts,
        'title': title
    }
    return render(request, 'posts/group_list.html', context)
