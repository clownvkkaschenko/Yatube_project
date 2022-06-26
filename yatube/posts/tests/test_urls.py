from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.core.cache import cache
from http import HTTPStatus
from posts.models import Post, Group


User = get_user_model()


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_author')

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.group = Group.objects.create(
            title='title test group',
            slug='test_slug',
            description='test description'
        )
        self.post = Post.objects.create(
            text='Test text',
            author=self.user,
            group=self.group
        )

    def test_urls_uses_correct_template(self):
        """URL-address uses the appropriate pattern."""
        cache.clear()
        templates_url_names = {
            '/': 'posts/index.html',
            '/create/': 'posts/create_post.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.post.author}/': 'posts/profile.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
            f'/posts/{self.post.id}/edit/': 'posts/create_post.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(
                    response,
                    template,
                    'Метод test_urls_uses_correct_template '
                    'работает неправильно.'
                )

    def test_of_accessible_pages(self):
        """Pages that are available to any user."""
        available_pages = {
            '/': HTTPStatus.OK,
            f'/group/{self.group.slug}/': HTTPStatus.OK,
            f'/profile/{self.post.author}/': HTTPStatus.OK,
            f'/posts/{self.post.id}/': HTTPStatus.OK,
            '/unexisting_page/': HTTPStatus.NOT_FOUND
        }
        for address, expected_status_code in available_pages.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address).status_code
                self.assertEqual(
                    response,
                    expected_status_code,
                    'Метод test_of_accessible_pages работает неправильно.'
                )

    def test_pages_available_to_authorized_user(self):
        """Pages available to an authorized user."""
        pages_available_to_authorized_users = [
            '/create/',
            f'/posts/{self.post.id}/edit/'
        ]
        for address in pages_available_to_authorized_users:
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    'Метод test_pages_available_to_authorized_user '
                    'работает неправильно.'
                )

    def test_page_list_url_redirect_anonymous(self):
        """Pages that redirect an unauthorized user."""
        pages_available_to_guest_client = [
            '/create/',
            f'/posts/{self.post.id}/edit/',
            f'/posts/{self.post.id}/comment/',
            f'/profile/{self.post.author}/follow/',
            f'/profile/{self.post.author}/unfollow/'
        ]
        for address in pages_available_to_guest_client:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.FOUND,
                    'Метод test_page_list_url_redirect_anonymous '
                    'работает неправильно.'
                )

    def test_page_list_url_redirect_authorized_client(self):
        """Pages that redirect an authorized user."""
        pages_available_to_guest_client = [
            f'/posts/{self.post.id}/comment/',
            f'/profile/{self.post.author}/follow/',
            f'/profile/{self.post.author}/unfollow/'
        ]
        for address in pages_available_to_guest_client:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.FOUND,
                    'Метод test_page_list_url_redirect_authorized_client '
                    'работает неправильно.'
                )
