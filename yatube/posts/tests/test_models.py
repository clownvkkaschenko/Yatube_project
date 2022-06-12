from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Post, Group

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост для проверки метода __str__'
        )

    def test_post_and_group_models_have_correct_object_names(self):
        """Checking, that __str__ works correctly for models."""
        post = self.post
        group = self.group
        field_verboses = {
            post.text[:15]: str(post),
            group.title: str(group)
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    value,
                    expected,
                    'Метод test_models_have_correct_object_names '
                    'работает неправильно.'
                )

    def test_group_verbose_name(self):
        """Group_verbose_name in the margins is the same as expected."""
        group = PostModelTest.group
        field_verboses = {
            'title': 'Имя сообщества',
            'slug': 'Адрес сообщества',
            'description': 'Описание сообщества',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).verbose_name,
                    expected_value,
                    'Метод test_group_verbose_name работает неправильно.'
                )

    def test_post_verbose_name(self):
        """Post_verbose_name in the margins is the same as expected."""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор поста',
            'group': 'Сообщество поста'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name,
                    expected_value,
                    'Метод test_post_verbose_name работает неправильно.'
                )
