# Generated by Django 2.2.6 on 2019-10-07 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainees', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainees',
            name='level',
            field=models.CharField(default='beginner', max_length=50),
        ),
    ]
