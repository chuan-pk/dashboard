from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime

def home_page(request):
    form_date = request.POST.get('date_picker')
    # change format here

    return render(request, 'dashboard/home.html',{
        'new_todo_text': request.POST.get('todo_text',''),
        'date_text': form_date,
    })
