# Generated by Django 3.0.3 on 2020-02-25 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_ingredient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='recipe',
        ),
    ]