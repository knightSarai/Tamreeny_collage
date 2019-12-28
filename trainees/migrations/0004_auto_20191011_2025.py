# Generated by Django 2.2.6 on 2019-10-11 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainees', '0003_trainees_future_elite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainees',
            name='level',
            field=models.CharField(choices=[('beginner', 'beginner'), ('intermediate', 'intermediate'), ('advanced', 'advanced'), ('elite', 'elite')], default='beginner', max_length=50),
        ),
    ]
