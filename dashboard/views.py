from django.shortcuts import render, redirect
from dashboard.models import Todolist

def home_page(request):

    #todo_list = Todolist()
    #todo_list.text = request.POST.get('todo_text','')
    #todo_list.date = request.POST.get('date_picker', '')
    #todo_list.prio = request.POST.get('priority', '')
    #todo_list.save()

    if request.method == 'POST':
        todo_text = request.POST['todo_text']
        todo_date = request.POST['date_picker']
        todo_prio = request.POST['priority']

        Todolist.objects.create(text=todo_text, date=todo_date, prio=todo_prio)
        return redirect('/')
    todo = Todolist.objects.all()
    return render(request, 'dashboard/home.html', {'todo': todo})
