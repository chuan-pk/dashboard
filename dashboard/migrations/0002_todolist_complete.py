# Generated by Django 2.0.1 on 2018-02-24 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='complete',
            field=models.TextField(default='False'),
        ),
    ]
