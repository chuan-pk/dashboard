from dashboard.New_calen import HTMLCalendar
from django.http import HttpResponse
from django.shortcuts import render, redirect
from dashboard.models import Todolist
from datetime import datetime

def home_page(request):

    if request.method == 'POST':
        todo_text = request.POST.get('todo_text', '')
        todo_date = request.POST.get('date_picker', '')       # send default value when user not input?
        todo_prio = request.POST.get('priority', '-')   #

        if len(todo_text) > 0:
            Todolist.objects.create(text=todo_text, date=todo_date, prio=todo_prio)
            return redirect('/')
    
    todo = Todolist.objects.filter(complete=False)
    complete = Todolist.objects.filter(complete=True)
    tc = HTMLCalendar()
    year = datetime.now().year
    month = datetime.now().month

    calen = tc.formatmonth(year, month)
    return render(request, 'dashboard/home.html', {'todo': todo, 'complete':complete, 'calendar':calen})

def delete_item(request, item_id):
    del_todo = Todolist.objects.get(id=item_id)
    del_todo.delete()
    return redirect('/')

def submit_item(request, item_id):
    submit_todo = Todolist.objects.get(id=item_id)
    submit_todo.complete = not(submit_todo.complete)
    submit_todo.save()
    return redirect('/')