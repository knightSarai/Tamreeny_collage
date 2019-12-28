from django.db import models
from trainees.models import Trainees
from datetime import datetime
from datetime import datetime


class ShapeData(models.Model):
    trainee = models.ForeignKey(Trainees, on_delete=models.CASCADE)
    classifier_counter = models.IntegerField()
    in_shape_counter = models.IntegerField(default=0)
    out_shape_counter = models.IntegerField(default=0)

    def __str__(self):
        return self.trainee.name


class Activity(models.Model):
    trainee = models.ForeignKey(Trainees, on_delete=models.CASCADE)
    inactive = models.DateTimeField(blank=True)
    active = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.trainee.name


class Progress(models.Model):
    beginner = 'beginner'
    intermediate = 'intermediate'
    advanced = 'advanced'
    elite = 'elite'
    LEVEL_CHOICES = [('beginner', beginner), (intermediate,
                                              'intermediate'), (advanced, 'advanced'), (elite, 'elite')]

    trainee = models.ForeignKey(Trainees, on_delete=models.CASCADE)
    level = models.CharField(
        max_length=50, choices=LEVEL_CHOICES, default=beginner, null=False)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.trainee.name


class Health(models.Model):
    trainee = models.ForeignKey(Trainees, on_delete=models.CASCADE)
    injure = models.DateTimeField(blank=True)
    recover = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.trainee.name


class PredictionResult(models.Model):
    trainee = models.ForeignKey(Trainees, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    vlaue = models.DecimalField(blank=True, max_digits=8, decimal_places=4)

    def __str__(self):
        return self.trainee.name
