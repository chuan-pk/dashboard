from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
    return render(request, 'dashboard/home.html', {
            'new_todo_text':request.POST.get('todo_text', '')
        })