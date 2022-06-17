from django.test import Client, TestCase
from http import HTTPStatus


class CorePagesTests(TestCase):
    def setUp(self):
        self.authorized_client = Client()

    def test_error_pages_uses_correct_template(self):
        """Error pages use the appropriate template."""
        response = self.client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, 'core/404.html')
