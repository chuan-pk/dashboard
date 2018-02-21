from django.test import TestCase
from django.urls import resolve
from dashboard import views as dashboard_views
from dashboard.models import Todolist
from selenium import webdriver 

class HomePageTest(TestCase):

    def test_can_save_post_request(self):
        response = self.client.post('/', data={'todo_text':'A new todo item', 'date_picker':'2018-03-13', 'priority':'Low'})
        
        self.assertEqual(Todolist.objects.count(), 1)
        
        todo = Todolist.objects.first()
        self.assertEqual(todo.text, 'A new todo item')
        self.assertEqual(todo.date, '2018-03-13')
        self.assertEqual(todo.prio, 'Low')

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'todo_text':'A new todo item', 'date_picker':'2018-03-13', 'priority':'Low'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Todolist.objects.count(), 0)

    def test_displays_all_list_items(self):
        Todolist.objects.create(text='itemey 1', date='2018-03-13', prio='Low')
        Todolist.objects.create(text='itemey 2', date='2018-02-24', prio='High')

        response = self.client.get('/')

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())

    def test_btn_delete(self):
        First_todo = Todolist.objects.create(text='itemey 1', date='2018-03-13', prio='Low')
        Secound_todo = Todolist.objects.create(text='itemey 2', date='2018-02-24', prio='High')

        response = self.client.post(f'/delete_item/{First_todo.id}')

        
        self.assertEqual(len(Todolist.objects.all()), 1)
        self.assertEqual(Todolist.objects.all()[0], Secound_todo)

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Todolist()
        first_item.text = 'The first (ever) list item'
        first_item.date = '2018-02-22'
        first_item.prio = 'High'
        first_item.save()

        second_item = Todolist()
        second_item.text = 'Item the second'
        second_item.date = '2018-02-26'
        second_item.prio = 'Low'
        second_item.save()

        saved_items = Todolist.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.date, '2018-02-22')
        self.assertEqual(first_saved_item.prio, 'High')
        
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.date, '2018-02-26')
        self.assertEqual(second_saved_item.prio, 'Low')

    def test_can_delete_item(self):
        Todolist.objects.create(text='itemey 1', date='2018-03-13', prio='Low')
        Todolist.objects.create(text='itemey 2', date='2018-02-24', prio='High')

        saved_items = Todolist.objects.all()
        saved_items[0].delete()

        self.assertEqual(Todolist.objects.count(), 1)