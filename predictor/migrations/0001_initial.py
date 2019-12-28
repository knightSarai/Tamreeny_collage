# Generated by Django 2.2.7 on 2019-12-10 11:55

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('trainees', '0010_workouts'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShapeData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classifier_counter', models.IntegerField()),
                ('in_shape_counter', models.IntegerField(default=0)),
                ('out_shape_counter', models.IntegerField(default=0)),
                ('trainee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainees.Trainees')),
            ],
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('beginner', 'beginner'), ('intermediate', 'intermediate'), ('advanced', 'advanced'), ('elite', 'elite')], default='beginner', max_length=50)),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('trainee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainees.Trainees')),
            ],
        ),
        migrations.CreateModel(
            name='PredictionResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('vlaue', models.DecimalField(blank=True, decimal_places=4, max_digits=8)),
                ('trainee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainees.Trainees')),
            ],
        ),
        migrations.CreateModel(
            name='Health',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('injure', models.DateTimeField(blank=True)),
                ('recover', models.DateTimeField(blank=True, null=True)),
                ('trainee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainees.Trainees')),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inactive', models.DateTimeField(blank=True)),
                ('active', models.DateTimeField(blank=True, null=True)),
                ('trainee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainees.Trainees')),
            ],
        ),
    ]
