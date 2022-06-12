import shutil
import tempfile

from django.contrib.auth import get_user_model
from posts.models import Post, Group
from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from http import HTTPStatus

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
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

    def test_creating_a_post_for_an_authorized_user(self):
        """Valid form creates an entry in Post."""
        posts_count = Post.objects.count()
        form_data = {
            'text': self.post.text,
            'group': self.group.id,
            'author': self.user.id
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        new_post = response.context['page_obj'][0]
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': self.post.author})
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(new_post.text, form_data['text'])
        self.assertEqual(new_post.group.id, form_data['group'])
        response_unauthorized_user = self.guest_client.get('/create/')
        self.assertEqual(
            response_unauthorized_user.status_code,
            HTTPStatus.FOUND,
        )

    def test_editing_the_post_of_the_author_of_the_message(self):
        """Valid form edit post author."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Сложная вещь, эти тесты...',
            'group': self.group.id,
            'author': self.user.id
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        post = response.context['posts']
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': self.post.id})
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group.id, form_data['group'])
        response_unauthorized_user = self.guest_client.get(
            f'/posts/{self.post.id}/edit/'
        )
        self.assertEqual(
            response_unauthorized_user.status_code,
            HTTPStatus.FOUND,
        )
