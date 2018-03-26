from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from django.test import LiveServerTestCase
import time
from dashboard.models import Todolist
from django.urls import resolve
from datetime import datetime


class ToDoListTest(LiveServerTestCase):
    """
    Dashboard Todo list test
    # = story
    ## = programmer's comment 
    """
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        time.sleep(1)
        self.browser.quit()
    
    def test_can_display_todo_list(self):

        # John H. Watson go to Student Dashboard web app
        # He notices the web app title
        self.browser.get(self.live_server_url)
        self.assertIn('Dashboard', self.browser.title)

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

        add_btn = self.browser.find_element_by_id('Add')


        # John add new todo item
        # He enter the text, select date, select priority
        # and click add button to add his todo list
        todo_text.send_keys('Do Analog Assignment')
        date_picker.click()
        date_picker.send_keys('2018-02-13')
        priority_picker.send_keys('High')
        add_btn.send_keys(Keys.ENTER)
        time.sleep(1)

        # He see the todo item in todo list
        table = self.browser.find_element_by_id('todo_table')
        rows = table.find_elements_by_tag_name('tr')
        rows_texts = [row.text for row in rows]
        ## check the row that contain 'Do analog..' '2018 ..' 'High' in same row
        self.assertTrue(
            any(('Do Analog Assignment' and '2018-02-13' and 'High') in i for i in  rows_texts)
            )

        # and see the submit and delete button of each list
        saved_todo = Todolist.objects.all()
        first_item = saved_todo[0]
        ## each to do list should have 2 type of button submit. delete
        ## and have unique id
        submit_button_list = self.browser.find_elements_by_id('submit')
        self.assertTrue(
            any(i.get_attribute('name') == str(first_item.id) for i in submit_button_list)
            )
        delete_button_list = self.browser.find_elements_by_id('delete')
        self.assertTrue(
            any(i.get_attribute('name') == str(first_item.id) for i in delete_button_list)
            )

        # John enter another todo item
        ## get all element to input
        todo_text = self.browser.find_element_by_id('new_todo')
        date_picker = self.browser.find_element_by_id('date_picker')
        priority_picker = self.browser.find_element_by_id('priority')
        add_btn = self.browser.find_element_by_id('Add')

        todo_text.send_keys('Think about Ubi.Com. project')
        date_picker.click()
        date_picker.send_keys('2018-02-27')
        priority_picker.send_keys('Low')
        add_btn.send_keys(Keys.ENTER)
        time.sleep(1)

        # John look at todo list and He see 2 items
        # 'Do assignment' and 'Ubi com project'
        # each item have 2 button submit and delete
        table = self.browser.find_element_by_id('todo_table')
        rows = table.find_elements_by_tag_name('tr')
        rows_texts = [row.text for row in rows]

        self.assertTrue(
            any('Do Analog Assignment' and '2018-02-13' and 'High' in i for i in  rows_texts), rows_texts
            )

        self.assertTrue(
            any('Think about Ubi.Com. project' and '2018-02-27' and 'Low' in i for i in  rows_texts), rows_texts
            ) 

        ## Check each object its has own button
        saved_todo = Todolist.objects.all()
        first_item = saved_todo[0]
        submit_button_list = self.browser.find_elements_by_id('submit')
        self.assertTrue(
            any(i.get_attribute('name') == str(first_item.id) for i in submit_button_list)
            )
        delete_button_list = self.browser.find_elements_by_id('delete')
        self.assertTrue(
            any(i.get_attribute('name') == str(first_item.id) for i in delete_button_list)
            )

        second_item = saved_todo[1]
        submit_button_list = self.browser.find_elements_by_id('submit')
        self.assertTrue(
            any(i.get_attribute('name') == str(second_item.id) for i in submit_button_list)
            )
        delete_button_list = self.browser.find_elements_by_id('delete')
        self.assertTrue(
            any(i.get_attribute('name') == str(second_item.id) for i in delete_button_list)
            )
        
        # John need to remove 'Do analog assignment' 
        # He won't see it anymore
        first_delete_btn = delete_button_list[0]
        first_delete_btn.click()

        table = self.browser.find_element_by_id('todo_table')
        rows = table.find_elements_by_tag_name('tr')
        rows_texts = [row.text for row in rows]

        self.assertFalse(
            any(('Do Analog Assignment' and '2018-02-13' and 'High') in i for i in  rows_texts), rows_texts
            )


    def test_default_date_and_priority_input(self):

        self.browser.get(self.live_server_url)

        todo_text = self.browser.find_element_by_id('new_todo')
        date_picker = self.browser.find_element_by_id('date_picker')
        priority_picker = self.browser.find_element_by_id('priority')
        add_btn = self.browser.find_element_by_id('Add')


        # John add 'Do Network assignment' but he forget to input date and priority
        ## our app should handle this case, so John can see his todo item with default value 
        todo_text.send_keys('Do Network assignment')
        todo_text.send_keys(Keys.ENTER)
        
        time.sleep(2)

        table = self.browser.find_element_by_id('todo_table')
        rows = table.find_elements_by_tag_name('tr')
        rows_texts = [row.text for row in rows]

        # the web page refresh and he will see 'Do Network assignment' with Default date and priority
        self.assertTrue(
            any(('Do Network assignment' and '' and '-') in i for i in  rows_texts), rows_texts
            )

        # John try to add the todo list but not priority
        todo_text = self.browser.find_element_by_id('new_todo')
        date_picker = self.browser.find_element_by_id('date_picker')
        priority_picker = self.browser.find_element_by_id('priority')
        add_btn = self.browser.find_element_by_id('Add')

        todo_text.send_keys('Do a research about SPEC-2006 benchmark suite')
        date_picker.click()
        date_picker.send_keys('2018-02-27')
        add_btn.send_keys(Keys.ENTER)

        self.assertTrue(
            any(('Do a research about SPEC-2006 benchmark suite' and '2018-02-27' and '-') in i for i in  rows_texts), rows_texts
            )

        time.sleep(1)

        # John not input the todo text and he hit the ENTER button
        # No blank list show in the todo table
        todo_text = self.browser.find_element_by_id('new_todo')
        date_picker = self.browser.find_element_by_id('date_picker')
        priority_picker = self.browser.find_element_by_id('priority')
        add_btn = self.browser.find_element_by_id('Add')

        todo_text.send_keys(Keys.ENTER)
        time.sleep(2)

        self.assertTrue(
            any(('Do Network assignment' and '' and '-') in i for i in  rows_texts), rows_texts
            )

        self.assertTrue(
            any(('Do a research about SPEC-2006 benchmark suite' and '2018-02-27' and '-') in i for i in  rows_texts), rows_texts
            )



    def test_submit_btn(self):

        self.browser.get(self.live_server_url)

        todo_text = self.browser.find_element_by_id('new_todo')
        date_picker = self.browser.find_element_by_id('date_picker')
        priority_picker = self.browser.find_element_by_id('priority')
        add_btn = self.browser.find_element_by_id('Add')

        todo_text.send_keys('Do Analog Assignment')
        date_picker.click()
        date_picker.send_keys('2018-02-13')
        priority_picker.send_keys('High')
        add_btn.send_keys(Keys.ENTER)
        time.sleep(1)

        todo_text = self.browser.find_element_by_id('new_todo')
        date_picker = self.browser.find_element_by_id('date_picker')
        priority_picker = self.browser.find_element_by_id('priority')
        add_btn = self.browser.find_element_by_id('Add')

        todo_text.send_keys('Think about Ubi.Com. project')
        date_picker.click()
        date_picker.send_keys('2018-02-27')
        priority_picker.send_keys('Low')
        add_btn.send_keys(Keys.ENTER)
        time.sleep(1)

        todo_text = self.browser.find_element_by_id('new_todo')
        date_picker = self.browser.find_element_by_id('date_picker')
        priority_picker = self.browser.find_element_by_id('priority')
        add_btn = self.browser.find_element_by_id('Add')

        todo_text.send_keys('Do a research about SPEC-2006 benchmark suite')
        date_picker.click()
        date_picker.send_keys('2018-02-27')
        add_btn.send_keys(Keys.ENTER)
        time.sleep(1)


        submit_button_list = self.browser.find_elements_by_id('submit')

        # now John finished analog assignment he want to submit it
        # he click submit button at the analog assignment row 
        first_submit_btn = submit_button_list[0]
        first_submit_btn.click()

        # he see the analog assignment in the complete table
        complete_table = self.browser.find_element_by_id('complete_table')
        complete_rows = complete_table.find_elements_by_tag_name('tr')
        complete_rows_texts = [row.text for row in complete_rows]

        self.assertTrue(
            any(('Do Analog Assignment' and '2018-02-13' and 'High') in i for i in  complete_rows_texts), complete_rows_texts
            )


        submit_button_list = self.browser.find_elements_by_id('submit')

        # John have an idea about Ubi.com project he click submit it
        # he click submit button at the analog assignment row 
        first_submit_btn = submit_button_list[0]
        first_submit_btn.click()

        # he see the analog assignment and think about ubi.com project in the complete table
        complete_table = self.browser.find_element_by_id('complete_table')
        complete_rows = complete_table.find_elements_by_tag_name('tr')
        complete_rows_texts = [row.text for row in complete_rows]
        
        self.assertTrue(
            any(('Do Analog Assignment' and '2018-02-13' and 'High') in i for i in  complete_rows_texts), complete_rows_texts
            )
        self.assertTrue(
            any('Think about Ubi.Com. project' and '2018-02-27' and 'Low' in i for i in  complete_rows_texts)
            ) 

        time.sleep(1)
        # but he not sure his ubi.com project is an good idea
        # he will do more research about ubi.com
        # so he unsubmit it

        unsubmit_button_list = self.browser.find_elements_by_id('unsubmit')

        # now John finished analog assignment he want to submit it
        # he click submit button at the analog assignment row 
        second_unsubmit_btn = unsubmit_button_list[1]
        second_unsubmit_btn.click()

        todo_table = self.browser.find_element_by_id('todo_table')
        todo_rows = todo_table.find_elements_by_tag_name('tr')
        todo_rows_texts = [row.text for row in todo_rows]

        # he see the analog assignment and think about ubi.com project in the complete table
        complete_table = self.browser.find_element_by_id('complete_table')
        complete_rows = complete_table.find_elements_by_tag_name('tr')
        complete_rows_texts = [row.text for row in complete_rows]

        self.assertTrue(
            any('Think about Ubi.Com. project' and '2018-02-27' and 'Low' in i for i in  todo_rows_texts)
            ) 
        self.assertTrue(
            any(('Do Analog Assignment' and '2018-02-13' and 'High') in i for i in  complete_rows_texts), complete_rows_texts
            )
        
    
    def test_can_display_calendar(self):
        
        # John see calendar of this month
        self.browser.get(self.live_server_url)
        calendar_table = self.browser.find_element_by_name('month')
        calendar_rows = calendar_table.find_elements_by_tag_name('tr')
        calendar_rows_texts = [row.text for row in calendar_rows]

        this_year = datetime.now().year
        this_month = datetime.now().month
        this_day = datetime.now().day

        ## Check this day, month and years
        self.assertTrue(
            any(str(this_year) in i for i in  calendar_rows_texts)
            )
        self.assertTrue(
            any(str(this_month) in i for i in  calendar_rows_texts)
            )
        self.assertTrue(
            any(str(this_day) in i for i in  calendar_rows_texts)
            )

        self.fail('Finish the test!')
        

if __name__ == '__main__':
    unittest.main(warnings='ignore')
