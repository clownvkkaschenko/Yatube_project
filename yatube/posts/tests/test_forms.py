import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from http import HTTPStatus
from posts.models import Post, Group, Follow


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

    def test_commenting_on_entries(self):
        """Only authorized users can comment."""
        form_data = {
            'text': 'test comment'
        }
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        new_comment = response.context['comments'][0]
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(new_comment.text, form_data['text'])
        self.assertEqual(new_comment.post.id, self.post.id)

    def test_creating_a_post_for_an_authorized_user(self):
        """Valid form creates an entry in Post."""
        posts_count = Post.objects.count()
        image = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='test.jpg',
            content=image,
            content_type='image/jpg'
        )
        form_data = {
            'text': self.post.text,
            'group': self.group.id,
            'author': self.user.id,
            'image': uploaded
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
        self.assertTrue(
            Post.objects.filter(
                image='posts/test.jpg'
            ).exists()
        )

    def test_creating_a_post_is_not_available_to_an_unauthorized_user(self):
        """Valid post creation form."""
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

    def test_editing_a_post_is_not_available_to_an_unauthorized_user(self):
        """Valid Post Edit Form."""
        response_unauthorized_user = self.guest_client.get(
            f'/posts/{self.post.id}/edit/'
        )
        self.assertEqual(
            response_unauthorized_user.status_code,
            HTTPStatus.FOUND,
        )
