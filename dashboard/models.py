from django.db import models

class Todolist(models.Model):
    text = models.TextField(default='')
    date = models.TextField(default='')
    prio = models.TextField(default='')
    complete = models.BooleanField(default=False)