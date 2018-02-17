from django.test import TestCase
from django.urls import resolve
from dashboard import views as dashboard_views

class HomePageTest(TestCase):

    def test_root_url_resovles_to_home_page_view(self):
        root = resolve('/')
        self.assertEqual(root.func, dashboard_views.home_page)

    def test_return_correct_html(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'dashboard/home.html')