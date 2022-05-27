from django.db import models
from django.contrib.auth import get_user_model
from posts.validators import validate_not_empty


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='Введите текст поста',
        validators = [validate_not_empty],
        )
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = 'posts')
    group = models.ForeignKey(
        Group,
        on_delete = models.SET_NULL,
        blank = True, null = True,
        related_name = 'group_list',
        help_text='Группа, к которой будет относиться пост',
        verbose_name='Группа',
        )

    class Meta:
        ordering = ['-pub_date']
    
    def __str__(self):
        return self.text
