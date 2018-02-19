from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime

def home_page(request):
    todo_text = request.POST.get('todo_text','')
    form_date = request.POST.get('date_picker', '')
    priority = request.POST.get('priority', '')
    # change format here

    return render(request, 'dashboard/home.html',{
        'new_todo_text': todo_text,
        'date_text': form_date,
        'priority': priority,
    })
