import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django import forms
from django.core.cache import cache
from http import HTTPStatus
from posts.models import Post, Group, Follow, Comment


User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
TOTAL_TEST_PAGES: int = 13
LMT_PSTS_FRST_PG: int = 10


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Автор тестов')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.user = User.objects.create_user(username='Ёжик')
        self.authorized_client.force_login(self.user)

        self.group = Group.objects.create(
            title='Сообщество для тестов',
            slug='tests_tests_and_tests',
            description='описание тестов'
        )
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
        self.post = Post.objects.create(
            text='Интересная, но сложная вещь, эти тесты...',
            author=self.user,
            group=self.group,
            image=uploaded
        )
        self.comments = Comment.objects.create(
            post=self.post,
            author=self.user,
            text='Тестовый комментарий'
        )

    def test_page_uses_correct_template(self):
        """URL-address uses the appropriate pattern."""
        cache.clear()
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
                    'posts/create_post.html',
            reverse('posts:follow_index'): 'posts/follow.html'
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

    def test_homepage_caching_check(self):
        """Checking the caching of the main page"""
        response_first = self.authorized_client.get(reverse('posts:index'))
        post = response_first.content
        Post.objects.create(
            text=self.post.text,
            author=self.post.author,
        )
        response_second = self.authorized_client.get(reverse('posts:index'))
        second_post = response_second.content
        self.assertEqual(post, second_post)
        cache.clear()
        response_third = self.authorized_client.get(reverse('posts:index'))
        third_post = response_third.content
        self.assertNotEqual(second_post, third_post)

    def test_index_page_show_correct_context(self):
        """The index template is formed with the correct context."""
        cache.clear()
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_image_0, self.post.image)

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
        post_image_0 = first_object.image
        self.assertEqual(group_title_0, self.post.group.title)
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_image_0, self.post.image)

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
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_author_0, self.post.author)
        self.assertEqual(post_image_0, self.post.image)

    def test_post_detail_page_show_correct_context(self):
        """The post_detail template is formed with the correct context."""
        response = self.authorized_client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id})
        )
        self.assertEqual(response.context.get('posts').text, self.post.text)
        self.assertEqual(response.context.get('posts').image, self.post.image)

    def test_post_create_page_show_correct_context(self):
        """The post_create template is formed with the correct context."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField
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
            'image': forms.fields.ImageField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_add_comment_page_show_correct_context(self):
        """The add_comment template is formed with the correct context."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        self.assertEqual(response.context['comments'][0].text, self.comments.text)


class FollowViewsTest(TestCase):
    """Subscription test."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='Автор')
        cls.subscriber = User.objects.create_user(username='Подписчик')

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

        self.authorized_client_two = Client()
        self.authorized_client_two.force_login(self.subscriber)

        self.post = Post.objects.create(
            text='Интересная, но сложная вещь, эти тесты...',
            author=self.author,
        )

    def test_subscription_to_the_selected_author(self):
        """The user can follow the author."""
        count_subscriptions = Follow.objects.count()
        response = self.authorized_client_two.get(
            reverse('posts:profile_follow', kwargs={
                'username': self.author.username}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Follow.objects.count(), count_subscriptions + 1)
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': self.author.username}))
        self.assertTrue(Follow.objects.filter(
            user=self.subscriber, author=FollowViewsTest.author
        ).exists())

    def test_unsubscribe_from_selected_author(self):
        """The user can unfollow the author."""
        Follow.objects.create(user=self.subscriber, author=self.author)
        count_subscriptions = Follow.objects.count()
        response = self.authorized_client_two.get(
            reverse('posts:profile_unfollow', kwargs={
                'username': self.author.username}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Follow.objects.count(), count_subscriptions - 1)
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': self.author.username}))
        self.assertFalse(Follow.objects.filter(
            user=self.subscriber, author=self.author
        ).exists())

    def test_posts_by_selected_authors(self):
        """Posts of selected authors are published in the feed."""
        Follow.objects.create(user=self.subscriber, author=self.author)
        response = self.authorized_client_two.get(
            reverse('posts:follow_index')
        )
        first_object = response.context['page_obj'][0]
        post_image_0 = first_object.image
        self.assertEqual(first_object, self.post)
        self.assertEqual(post_image_0, self.post.image)


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
        self.post = Post.objects.bulk_create(
            [
                Post(
                    text='Интересная, но сложная вещь, эти тесты...',
                    author=self.user,
                    group=self.group,
                ),
            ] * TOTAL_TEST_PAGES
        )

    def test_first_page_contains_ten_records(self):
        """The number of posts on the first page is 10."""
        paginators_list = {
            reverse('posts:index'): LMT_PSTS_FRST_PG,
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}): LMT_PSTS_FRST_PG,
            reverse(
                'posts:profile',
                kwargs={'username': self.user.username}): LMT_PSTS_FRST_PG,
        }
        for reverse_name, cnt_of_posts in paginators_list.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(
                    len(response.context['page_obj']), cnt_of_posts
                )

    def test_first_page_contains_ten_records(self):
        """The number of posts on the second page is 3."""
        all_posts = Post.objects.filter(
            author__username=self.user.username
        ).count()
        lmt_psts_scnd_pg: int = all_posts - LMT_PSTS_FRST_PG
        paginators_list = {
            reverse('posts:index'): lmt_psts_scnd_pg,
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}): lmt_psts_scnd_pg,
            reverse(
                'posts:profile',
                kwargs={'username': self.user.username}): lmt_psts_scnd_pg,
        }
        for reverse_name, cnt_of_posts in paginators_list.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(
                    reverse_name + '?page=2'
                )
                self.assertEqual(
                    len(response.context['page_obj']), cnt_of_posts
                )
