from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    """Class for creating groups."""
    title = models.CharField('Имя сообщества', max_length=200)
    slug = models.SlugField('Адрес сообщества', unique=True)
    description = models.TextField('Описание сообщества')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(models.Model):
    """Class for creating posts."""
    text = models.TextField('Текст поста')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор поста'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='group_list',
        verbose_name='Сообщество поста',
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.text[:15]
