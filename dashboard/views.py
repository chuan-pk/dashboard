from django.http import HttpResponse
from django.shortcuts import render, redirect
from dashboard.models import Todolist

def home_page(request):

    if request.method == 'POST':
        todo_text = request.POST.get('todo_text', '')
        todo_date = request.POST.get('date_picker', '')
        todo_prio = request.POST.get('priority', '')

        Todolist.objects.create(text=todo_text, date=todo_date, prio=todo_prio)
        return redirect('/')
    todo = Todolist.objects.all()
    return render(request, 'dashboard/home.html', {'todo': todo})

def delete_item(request, item_id):
    del_todo = Todolist.objects.get(id=item_id)
    del_todo.delete()
    return redirect('/')
