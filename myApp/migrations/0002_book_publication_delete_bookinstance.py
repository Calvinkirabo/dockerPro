# Generated by Django 4.0.6 on 2022-08-19 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='publication',
            field=models.CharField(default=0, max_length=40),
        ),
        migrations.DeleteModel(
            name='BookInstance',
        ),
    ]
