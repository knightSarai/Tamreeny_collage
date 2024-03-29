# Generated by Django 2.2.6 on 2019-10-22 11:17

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trainees', '0007_physical_attribute_l_set'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shape_state',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('classifier_level', models.CharField(choices=[('beginner', 'beginner'), ('intermediate', 'intermediate'), ('advanced', 'advanced'), ('elite', 'elite')], default='beginner', max_length=50)),
                ('previous_levl', models.CharField(choices=[('beginner', 'beginner'), ('intermediate', 'intermediate'), ('advanced', 'advanced'), ('elite', 'elite')], default='beginner', max_length=50)),
                ('trainee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='trainees.Trainees')),
            ],
        ),
    ]
