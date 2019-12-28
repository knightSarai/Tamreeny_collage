from django.db import models
from datetime import datetime
from trainers.models import Trainer


class Trainees(models.Model):
    beginner = 'beginner'
    intermediate = 'intermediate'
    advanced = 'advanced'
    elite = 'elite'
    trainer = models.ForeignKey(Trainer, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50, null=False)
    LEVEL_CHOICES = [('beginner', beginner), (intermediate,
                                              'intermediate'), (advanced, 'advanced'), (elite, 'elite')]
    level = models.CharField(
        max_length=50, choices=LEVEL_CHOICES, default=beginner, null=False)
    initialLevel = models.CharField(
        max_length=50, choices=LEVEL_CHOICES, default=beginner, null=False)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, help_text='your phone')
    roll_date = models.DateTimeField(default=datetime.now, blank=True)
    birthDay = models.DateTimeField(default=datetime.now, blank=True)
    note = models.TextField(blank=True)
    gender = models.CharField(max_length=100, null=True)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    is_active = models.BooleanField(default=True)
    shape = models.BooleanField(default=True)
    health_issue = models.BooleanField(default=True)
    future_elite = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    # def age


class Physical_attribute(models.Model):
    trainee = models.ForeignKey(Trainees, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(default=datetime.now, blank=True)
    push_ups = models.IntegerField(blank=True)
    pull_ups = models.IntegerField(blank=True)
    dips = models.IntegerField(blank=True)
    handstand = models.DecimalField(blank=True, max_digits=8, decimal_places=4)
    muscle_up = models.IntegerField(blank=True)
    deadlifts = models.IntegerField(blank=True)
    squat = models.IntegerField(blank=True)
    bench_press = models.IntegerField(blank=True)
    run = models.DecimalField(blank=True, max_digits=6, decimal_places=4)
    l_set = models.DecimalField(
        default=0, blank=True, max_digits=8, decimal_places=4)

    def __str__(self):
        return self.trainee.name


class Workouts(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    trainee = models.ForeignKey(Trainees, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now, blank=True)
    content = models.TextField(blank=True)


class Shape_state(models.Model):
    beginner = 'beginner'
    intermediate = 'intermediate'
    advanced = 'advanced'
    elite = 'elite'
    LEVEL_CHOICES = [('beginner', beginner), (intermediate,
                                              'intermediate'), (advanced, 'advanced'), (elite, 'elite')]

    trainee = models.ForeignKey(Trainees, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(default=datetime.now, blank=True)
    classifier_level = models.CharField(
        max_length=50, choices=LEVEL_CHOICES, default=beginner, null=False)
    previous_level = models.CharField(
        max_length=50, choices=LEVEL_CHOICES, default=beginner, null=False)
