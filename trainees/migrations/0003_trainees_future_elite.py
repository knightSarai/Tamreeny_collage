# Generated by Django 2.2.6 on 2019-10-10 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainees', '0002_trainees_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainees',
            name='future_elite',
            field=models.BooleanField(default=False),
        ),
    ]