# Generated by Django 2.2.6 on 2019-10-18 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('health_app', '0011_solutions_issues'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solutions',
            name='issues',
        ),
    ]
