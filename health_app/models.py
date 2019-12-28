from django.db import models
from datetime import datetime
from trainees.models import Trainees
from django.urls import reverse


class Issues(models.Model):
    code = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True)
    solve_ability = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse('health_app:issue-details', kwargs={'id': self.id})


class Solutions(models.Model):
    code = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.code


class Solution_list(models.Model):
    is_valid = models.BooleanField(default=True)
    issue = models.ForeignKey(Issues, on_delete=models.CASCADE)
    solution = models.ForeignKey(Solutions, on_delete=models.CASCADE)

    def __str__(self):
        return self.issue.code


class Trainees_health_issues(models.Model):
    trainee = models.ForeignKey(Trainees, on_delete=models.CASCADE)
    healed = models.BooleanField(default=False)
    issue = models.ForeignKey(Issues, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.trainee.name

    def get_absolute_url(self):
        return reverse('health_app:trainee-issue-details', kwargs={'id': self.id})
