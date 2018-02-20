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

    def test_can_save_post_request(self):
        response = self.client.post('/', data={'todo_text':'A new todo item', 'date_picker':'2018-03-13', 'priority':'Low'})
        self.assertContains(response, 'A new todo item')
        self.assertContains(response, '2018-03-13')
        self.assertContains(response, 'Low')
        self.assertTemplateUsed(response, 'dashboard/home.html')