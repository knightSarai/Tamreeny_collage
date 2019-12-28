from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages, auth
import numpy as np
import skfuzzy as fuzz
from trainees.models import Trainees
from .models import *
from datetime import datetime, timezone
import operator
import functools


def index(request, trainee_id):
    single_trainee = get_object_or_404(Trainees, pk=trainee_id)
    currentLvl = single_trainee.level
    if currentLvl == 'elite':
        messages.error(
            request, 'Trainee Already Elite')
        return redirect('/trainees/'+str(trainee_id))
    now = datetime.now(timezone.utc)
    dateRole = single_trainee.roll_date
    role = now - dateRole
    trainee_id = trainee_id
    birthday = single_trainee.birthDay
    t_age = int((now - birthday).days/360)

    # shape
    shape = ShapeData.objects.all().filter(trainee__id=trainee_id)
    if shape:
        shape = shape[0]
        classifierCounter = shape.classifier_counter
        inShapeCounter = shape.in_shape_counter
        shapePercantage = inShapeCounter / classifierCounter
        if shapePercantage == 1:
            shape = 10
        else:
            shape = float(str(shapePercantage - int(shapePercantage))[2:5])
    else:
        messages.error(
            request, 'You MUST make physique test first')
        return redirect('/trainees/'+str(trainee_id))

    # active
    inactive = Activity.objects.all().filter(trainee__id=trainee_id)
    if inactive:
        totalInacPeriods = [inActive.active -
                            inActive.inactive for inActive in inactive]
        totalInacPeriods = functools.reduce(operator.add, totalInacPeriods)
        inactivePercnt = totalInacPeriods / role
        active = 10 - float(str(inactivePercnt - int(inactivePercnt))[2:3])
    else:
        active = 10.0

    # progress speed
    progress_speed = Progress.objects.all().filter(trainee__id=trainee_id)
    lvl = str(single_trainee.initialLevel)
    if progress_speed:
        progress_speed = progress_speed[0]
        progress_speed = int((dateRole - progress_speed.date).days)
        trainee = ProgressRatio(lvl, progress_speed, t_age)
        if lvl == 'advanced':
            progress_speed = 1
        else:
            progress_speed = trainee.ratio()
    else:
        progress_speed = 1
        trainee = ProgressRatio(lvl, progress_speed, t_age)

    # health
    injure = Health.objects.all().filter(trainee__id=trainee_id)
    if injure:
        totalinjurePeriods = [
            Injure.recover - Injure.injure for Injure in injure if Injure.recover]

        totalinjurePeriods = functools.reduce(operator.add, totalinjurePeriods)

        injurePercnt = totalinjurePeriods / role
        health = float(str(injurePercnt - int(injurePercnt))[2:3])
    else:
        health = 0

    # age
    age = trainee.age_ratio()

    x_shape = np.arange(0, 11, 1)
    x_active = np.arange(0, 11, 1)
    x_progress_speed = np.arange(0, 11, 1)
    x_health = np.arange(0, 11, 1)
    x_age = np.arange(0, 11, 1)
    #! Output
    x_elite = np.arange(0, 11, 1)

    # - Generate fuzzy membership functions
    shape_lo = fuzz.trimf(x_shape, [0, 0, 5])
    shape_md = fuzz.trimf(x_shape, [0, 5, 10])
    shape_hi = fuzz.trimf(x_shape, [5, 10, 10])

    active_lo = fuzz.trimf(x_active, [0, 0, 5])
    active_md = fuzz.trimf(x_active, [0, 5, 10])
    active_hi = fuzz.trimf(x_active, [5, 10, 10])

    progress_speed_lo = fuzz.trimf(x_progress_speed, [0, 0, 5])
    progress_speed_md = fuzz.trimf(x_progress_speed, [0, 5, 10])
    progress_speed_hi = fuzz.trimf(x_progress_speed, [5, 10, 10])

    health_lo = fuzz.trimf(x_health, [0, 0, 5])
    health_md = fuzz.trimf(x_health, [0, 5, 10])
    health_hi = fuzz.trimf(x_health, [5, 10, 10])

    age_lo = fuzz.trimf(x_age, [0, 0, 5])
    age_md = fuzz.trimf(x_age, [0, 5, 10])
    age_hi = fuzz.trimf(x_age, [5, 10, 10])

    #! output Mempership Fn.
    elite_lo = fuzz.trimf(x_elite, [0, 0, 3])
    elite_alo = fuzz.trimf(x_elite, [2, 3, 4])
    elite_md = fuzz.trimf(x_elite, [3, 5, 7])
    elite_shi = fuzz.trimf(x_elite, [6, 7, 8])
    elite_hi = fuzz.trimf(x_elite, [7, 10, 10])

    shape_level_lo = fuzz.interp_membership(x_shape, shape_lo, shape)
    shape_level_md = fuzz.interp_membership(x_shape, shape_md, shape)
    shape_level_hi = fuzz.interp_membership(x_shape, shape_hi, shape)
    active_level_lo = fuzz.interp_membership(x_active, active_lo, active)
    active_level_md = fuzz.interp_membership(x_active, active_md, active)
    active_level_hi = fuzz.interp_membership(x_active, active_hi, active)
    progress_level_speed_lo = fuzz.interp_membership(
        x_progress_speed, progress_speed_lo, progress_speed)
    progress_level_speed_md = fuzz.interp_membership(
        x_progress_speed, progress_speed_md, progress_speed)
    progress_level_speed_hi = fuzz.interp_membership(
        x_progress_speed, progress_speed_hi, progress_speed)
    health_level_lo = fuzz.interp_membership(x_health, health_lo, health)
    health_level_md = fuzz.interp_membership(x_health, health_md, health)
    health_level_hi = fuzz.interp_membership(x_health, health_hi, health)
    age_level_lo = fuzz.interp_membership(x_age, age_lo, age)
    age_level_md = fuzz.interp_membership(x_age, age_md, age)
    age_level_hi = fuzz.interp_membership(x_age, age_hi, age)

    # - rule One
    rule1 = np.fmax(shape_level_lo, active_level_lo)
    # Now we apply this by clipping the top off the corresponding output
    # membership function with `np.fmin`
    elite_activation_lo = np.fmin(rule1, elite_lo)  # removed entirely to 0

    # - rule Two
    rule2 = np.fmax(shape_level_md, active_level_md)
    elite_activation_alo = np.fmin(rule2, elite_alo)

    # - rule Three
    rule3 = np.fmin(np.fmin(np.fmin(shape_level_hi, active_level_hi),
                            progress_level_speed_hi), health_level_lo)
    elite_activation_hi = np.fmin(rule3, elite_hi)

    # - rule four
    rule4 = np.fmax(np.fmin(np.fmin(shape_level_hi, active_level_hi), np.fmax(
        progress_level_speed_md, age_level_md)), health_level_md)
    elite_activation_md = np.fmin(rule4, elite_md)

    # - rule Five
    rule5 = np.fmax(np.fmin(np.fmax(shape_level_hi, active_level_hi), np.fmax(
        progress_level_speed_hi, age_level_hi)), health_level_hi)
    elite_activation_shi = np.fmin(rule5, elite_shi)
    aggregated = np.fmax(elite_activation_lo, np.fmax(elite_activation_alo, np.fmax(
        elite_activation_hi, np.fmax(elite_activation_md, elite_activation_shi))))

    elite = fuzz.defuzz(x_elite, aggregated, 'centroid')
    print('result', elite)
    if elite >= 5:
        single_trainee.future_elite = True
        single_trainee.save()
    else:
        single_trainee.future_elite = False
        single_trainee.save()

    result = PredictionResult(trainee_id=trainee_id, vlaue=elite)
    result.save()

    return redirect('/trainees/'+str(trainee_id))


class ProgressRatio:
    def __init__(self, initialLvl, progressSpeed, age):
        self.initialLvl = initialLvl
        self.progressSpeed = progressSpeed
        self.age = age

    def ratio(self):
        """ ALL in terms of days """
        if self.initialLvl == 'beginner':
            if self.progressSpeed > 810:
                return 3
            elif self.progressSpeed in range(720, 811):
                return 4
            elif self.progressSpeed in range(660, 720):
                return 5
            elif self.progressSpeed in range(540, 660):
                return 6
            elif self.progressSpeed in range(450, 540):
                return 7
            elif self.progressSpeed in range(420, 450):
                return 8
            elif self.progressSpeed in range(360, 420):
                return 9
            elif self.progressSpeed < 360:
                return 10

        elif self.initialLvl == 'intermediate':
            if self.progressSpeed > 360:
                return 3
            elif self.progressSpeed in range(300, 360):
                return 4
            elif self.progressSpeed in range(240, 300):
                return 5
            elif self.progressSpeed in range(210, 240):
                return 6
            elif self.progressSpeed in range(180, 210):
                return 7
            elif self.progressSpeed in range(150, 180):
                return 8
            elif self.progressSpeed in range(120, 150):
                return 9
            elif self.progressSpeed < 120:
                return 10
        else:
            return 5

    def age_ratio(self):
        if self.age < 10:
            return 1
        elif self.age in range(10, 13):
            return 2
        elif self.age in range(10, 13):
            return 3
        elif self.age in range(13, 16):
            return 4
        elif self.age in range(16, 18):
            return 5
        elif self.age in range(16, 18):
            return 6
        elif self.age in range(18, 21):
            return 7
        elif self.age in range(21, 23):
            return 8
        elif self.age in range(23, 25):
            return 9
        elif self.age in range(25, 26):
            return 9.5
        else:
            return 10


# def ratio(lvl, speed):
#         """ ALL in terms of days """
#         if lvl == 'beginner':
#             print('in beg')
#             if speed > 810:
#                 return 3
#             elif speed in range(720,811):
#                 return 4
#             elif speed in range(660,720):
#                 return 5
#             elif speed in range(540,660):
#                 return 6
#             elif speed in range(450,540):
#                 return 7
#             elif speed in range(420,450):
#                 return 8
#             elif speed in range(360,420):
#                 return 9
#             elif speed < 360:
#                 return 10

#         elif lvl == 'intermediate':
#             print('in inter')
#             if speed > 360:
#                 return 3
#             elif speed in range(300,360):
#                 return 4
#             elif speed in range(240,300):
#                 return 5
#             elif speed in range(210,240):
#                 return 6
#             elif speed in range(180,210):
#                 return 7
#             elif speed in range(150,180):
#                 return 8
#             elif speed in range(120,150):
#                 return 9
#             elif speed < 120:
#                 return 10
#         else:
#             return 5
