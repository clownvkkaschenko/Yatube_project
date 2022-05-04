from django.shortcuts import render, get_object_or_404

from .models import Post, Group


def index(request):
    posts = Post.objects.order_by('-pub_date')[:10]
    context = {
        'posts': posts,
        'title': 'Главная страница',
        'text': 'Последние обновления на сайте'
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    # Метод .filter позволяет ограничить поиск по критериям.
    # Это аналог добавления
    # условия WHERE group_id = {group_id}
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'group': group,
        'posts': posts,
        'title': f'Записи сообщества {group.title}'
    }
    return render(request, 'posts/group_list.html', context)
