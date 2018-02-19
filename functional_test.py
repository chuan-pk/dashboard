from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import unittest
import time


class ToDoListTest(unittest.TestCase):
    """
    Dashboard Todo list test
    app name: Dashboard
    # = story
    ## = programmer's comment 
    """

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        time.sleep(2)
        self.browser.quit()

    def test_can_display_todo_list(self):
        # Student name : John Doe 
        # John Doe go to Student Dashboard web app
        # He notices the web app title

        self.browser.get('http://localhost:8000/')
        self.assertIn('Dashboard', self.browser.title)

        ## check only to-do list 
        ## Dashboard will comming soon
        ## input : text, date&time picker, priority, submit button
        ## in progress : subject tag?

        # He notices the to-do list app header and input
        h1_list = [i.text for i in self.browser.find_elements_by_tag_name('h1')]
        self.assertTrue(
            any('Todo' in i for i in h1_list), 'Todo no found in' + str(h1_list)
            )
        self.assertTrue(
            any('Complete' in i for i in h1_list), 'Complete not found in' + str(h1_list)
            )

        # He look at the input of to-do item title
        todo_text = self.browser.find_element_by_id('new_todo')
        self.assertEqual(todo_text.get_attribute('placeholder'), 'Enter a to-do item')

        # He look at the date picker
        date_picker = self.browser.find_element_by_id('date_picker')
        self.assertEqual(date_picker.get_attribute('placeholder'), 'Select date')

        # He look at the priority picker
        priority_picker = self.browser.find_element_by_id('priority')
        # click on it and it will show the priority option High Medium and Low
        priority_list = self.browser.find_elements_by_tag_name('option')
        priority_value_list = [item.get_attribute('value') for item in priority_list]
        self.assertIn('High', priority_value_list)
        self.assertIn('Medium', priority_value_list)
        self.assertIn('Low', priority_value_list)
        ## smoke test of selet list 
        # self.assertIn('Wadu', priority_value_list)

        submit_btn = self.browser.find_element_by_id('submit')


        # John try to add new to do list and he will see the item in to-do 
        # enter the text, select date, select priority
        # and submit
        todo_text.send_keys('Do Analog Assignment')
        time.sleep(0.2)

        date_picker.click()
        time.sleep(0.01)
        date_picker.send_keys('2018-02-13')
        time.sleep(3)

        priority_picker.send_keys('High')
        time.sleep(0.2)

        submit_btn.send_keys(Keys.ENTER)
 
        table = self.browser.find_element_by_id('todo_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any('Do Analog Assignment' in i for i in [row.text for row in rows] )
            )



        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')