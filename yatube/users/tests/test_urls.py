from django.contrib.auth import get_user_model
from django.test import TestCase, Client


User = get_user_model()


class UserPagesURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_author')

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_user_of_accessible_pages(self):
        """Address availability check."""
        available_pages = {
            '/auth/signup/': 'users/signup.html',
            '/auth/logout/': 'users/logged_out.html',
            '/auth/login/': 'users/login.html',
            '/auth/reset/done/': 'users/password_reset_complete.html',
        }
        for address, template in available_pages.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(
                    response,
                    template,
                    'Метод test_user_of_accessible_pages '
                    'работает неправильно.'
                )
