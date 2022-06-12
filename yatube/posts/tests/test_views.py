from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Post, Group

User = get_user_model()
LMT_PSTS_FRST_PG: int = 10
LMT_PSTS_SCND_PG: int = 3


class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Автор тестов')

    def setUp(self):
        self.authorized_client = Client()
        self.user = User.objects.create_user(username='Ёжик')
        self.authorized_client.force_login(self.user)
        self.group = Group.objects.create(
            title='Сообщество для тестов',
            slug='tests_tests_and_tests',
            description='описание тестов'
        )
        self.post = Post.objects.create(
            text='Интересная, но сложная вещь, эти тесты...',
            author=self.user,
            group=self.group
        )

    def test_page_uses_correct_template(self):
        """URL-address uses the appropriate pattern."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': self.post.group.slug}):
                    'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': self.post.author}):
                    'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}):
                    'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.id}):
                    'posts/create_post.html'
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(
                    response,
                    template,
                    'Метод test_page_uses_correct_template '
                    'работает неправильно.'
                )

    def test_index_page_show_correct_context(self):
        """The index template is formed with the correct context."""
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        self.assertEqual(post_text_0, self.post.text)

    def test_group_list_page_show_correct_context(self):
        """The group_list template is formed with the correct context."""
        response = self.authorized_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': self.post.group.slug})
        )
        first_object = response.context['page_obj'][0]
        group_title_0 = first_object.group.title
        post_text_0 = first_object.text
        self.assertEqual(group_title_0, self.post.group.title)
        self.assertEqual(post_text_0, self.post.text)

    def test_profile_page_show_correct_context(self):
        """The profile template is formed with the correct context."""
        response = self.authorized_client.get(
            reverse(
                'posts:profile',
                kwargs={'username': self.post.author})
        )
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_author_0, self.post.author)

    def test_post_detail_page_show_correct_context(self):
        """The post_detail template is formed with the correct context."""
        response = self.authorized_client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id})
        )
        self.assertEqual(response.context.get('posts').text, self.post.text)

    def test_post_create_page_show_correct_context(self):
        """The post_create template is formed with the correct context."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_page_show_correct_context(self):
        """The post_edit template is formed with the correct context."""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id})
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)


class PaginatorViewsTest(TestCase):
    """Paginator testing."""
    def setUp(self):
        self.user = User.objects.create_user(username='Ёжик')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.group = Group.objects.create(
            title='Сообщество для тестов',
            slug='tests_tests_and_tests',
            description='описание тестов'
        )
        self.post = Post.objects.create(
            text='Интересная, но сложная вещь, эти тесты...',
            author=self.user,
            group=self.group
        )
        for v in range(1, 13):
            self.post = Post.objects.create(
                text=f'Тест номер {v}',
                author=self.user,
                group=self.group
            )

    def test_first_page_contains_ten_records(self):
        """The number of posts on the first page is 10."""
        paginators_list = {
            reverse('posts:index'): LMT_PSTS_FRST_PG,
            reverse(
                'posts:group_list',
                kwargs={'slug': self.post.group.slug}): LMT_PSTS_FRST_PG,
            reverse(
                'posts:profile',
                kwargs={'username': self.post.author}): LMT_PSTS_FRST_PG,
        }
        for reverse_name, cnt_of_posts in paginators_list.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(
                    len(response.context['page_obj']), cnt_of_posts
                )

    def test_first_page_contains_ten_records(self):
        """The number of posts on the second page is 3."""
        paginators_list = {
            reverse('posts:index'): LMT_PSTS_SCND_PG,
            reverse(
                'posts:group_list',
                kwargs={'slug': self.post.group.slug}): LMT_PSTS_SCND_PG,
            reverse(
                'posts:profile',
                kwargs={'username': self.post.author}): LMT_PSTS_SCND_PG,
        }
        for reverse_name, cnt_of_posts in paginators_list.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(
                    reverse_name + '?page=2'
                )
                self.assertEqual(
                    len(response.context['page_obj']), cnt_of_posts
                )
