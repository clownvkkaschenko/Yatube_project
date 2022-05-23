from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from .models import Post, Group

LMT_PSTS: int = 10  # limit posts per page


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.select_related('group').all()
    paginator = Paginator(posts, 10)
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
    posts = group.group_list.all()[:LMT_PSTS]
    title = f'Группа {group.title}'
    context = {
        'group': group,
        'posts': posts,
        'title': title
    }
    return render(request, template, context)
