from django.test import TestCase, Client
from http import HTTPStatus


class AboutPagesURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()


    def test_about_urls_uses_correct_template(self):
        """URL-application address about use the corresponding pattern."""
        templates_url_names = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
            '/about/exit/': 'about/exit.html'
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(
                    response,
                    template,
                    'Метод test_about_urls_uses_correct_template '
                    'работает неправильно.'
                )


    def test_about_of_accessible_pages(self):
        """Address availability check."""
        available_pages = {
            '/about/author/': HTTPStatus.OK,
            '/about/tech/': HTTPStatus.OK,
            '/about/exit/': HTTPStatus.OK,
        }
        for address, expected_status_code in available_pages.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address).status_code
                self.assertEqual(
                    response,
                    expected_status_code,
                    'Метод test_about_of_accessible_pages '
                    'работает неправильно.'
                )
