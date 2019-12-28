from django.db import models
from datetime import datetime


class Trainer(models.Model):
    name = models.CharField(max_length=50, null=False)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d')
    phone = models.CharField(max_length=20, help_text='your phone')
    description = models.TextField(blank=True)
    email = models.EmailField()
    is_mvp = models.BooleanField(default=False)
    hire_date = models.DateTimeField(default=datetime.now, blank=True)
    speciality = models.CharField(max_length=100)

    def __str__(self):
        return self.name
