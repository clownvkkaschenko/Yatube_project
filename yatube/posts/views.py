from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    template = 'posts/index.html'
    return render(request, template)

def group_posts(request, slug):
    template = 'posts/group_list.html'
    context = {
        'title': 'Group',
        'text': f'Test group {slug}',
    }
    return render(request, template, context)
