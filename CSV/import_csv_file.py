import csv
from dashboard.models import Todolist

with open('CSV/Todo_csv.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    next(csv_reader)

    for line in csv_reader:
        item = Todolist()
        item.text = line[0]
        item.date = line[1]
        item.prio = line[2]
        item.save()

# https://stackoverflow.com/questions/41266322/accessing-django-models-from-a-new-script
