from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # main page
    path('', views.index, name='index'),
    # group page
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
    # profile page
    path('profile/<str:username>/', views.profile, name='profile'),
    # page selected post
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    # creating a post
    path('create/', views.post_create, name='post_create'),
    # post editing
    path('posts/<post_id>/edit/', views.post_edit, name='post_edit'),
]
