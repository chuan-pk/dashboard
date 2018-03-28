import csv
from dashboard.models import Todolist

with open('CSV/Export_todo_csv.csv', 'w') as csv_file:
    field_name = ['text', 'due', 'prior']

    csv_writer = csv.DictWriter(csv_file, fieldnames=field_name, delimiter='\t')
    csv_writer.writeheader()

    Database_items = Todolist.objects.all()

    for item in Database_items:
        csv_writer.writerow({'text':item.text, 'due':item.date, 'prior':item.prio})


# https://stackoverflow.com/questions/41266322/accessing-django-models-from-a-new-script
