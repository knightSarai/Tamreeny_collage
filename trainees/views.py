from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from trainees.models import Trainees, Physical_attribute, Shape_state, Workouts
from trainers.models import Trainer
from health_app.models import Trainees_health_issues, Solution_list, Issues
from trainees.classifier import *
from predictor.models import *
from datetime import datetime, timezone

def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError

@login_required
def index(request):
    trainees_list = Trainees.objects.order_by(
        '-roll_date').filter(is_active=True)
    now = datetime.now(timezone.utc)
    for trainee in trainees_list:
        name = trainee.name
        trainee_health = Trainees_health_issues.objects.order_by(
            'issue_date').filter(trainee__name=name).filter(healed=False)

        if trainee_health:
            # for t in trainee_health:
            trainee.health_issue = True
            trainee.save()
            healthTrack = Health.objects.order_by('-injure').filter(trainee_id= trainee.id)
            if healthTrack:
                healthTrack = healthTrack[0]
                if healthTrack.recover:
                    healthTrack = Health(trainee_id= trainee.id ,injure=now)
                    healthTrack.save()
                else:
                    healthTrack.recover = now
                    healthTrack.save()
            else:
                healthTrack = Health(trainee_id= trainee.id ,injure=now)
                healthTrack.save()
        else:
            trainee.health_issue = False
            trainee.save()
            healthTrack = Health.objects.order_by('-injure').filter(trainee_id= trainee.id)
            if healthTrack:
                healthTrack = healthTrack[0]
                if not healthTrack.recover:
                    healthTrack.recover = now
                    healthTrack.save()

    paginator = Paginator(trainees_list, 6)
    page = request.GET.get('page')
    paged_listing = paginator.get_page(page)

    context = {
        'trainees_list': paged_listing
    }
    return render(request, 'trainees/trainees.html', context)


@login_required
def trainee(request, trainee_id):
    single_trainee = get_object_or_404(Trainees, pk=trainee_id)
    name = single_trainee.name
    now = datetime.now(timezone.utc)
    birthday = single_trainee.birthDay
    t_age = int((now - birthday).days/360)

    # level = single_trainee.level
    # if level == 'elite':
    #     level = True
    # else:
    #     level = False

    elite = PredictionResult.objects.order_by(
        '-date').filter(trainee__id=trainee_id)
    if elite:
        elite = elite[0]
        if elite.vlaue >= 5:
            single_trainee.future_elite = True
            single_trainee.save()
        else:
            single_trainee.future_elite = False
            single_trainee.save()
    else:
        single_trainee.future_elite = False
        single_trainee.save()

    issues = Trainees_health_issues.objects.order_by(
        'issue_date').filter(trainee__name=name).filter(healed=False)
    if issues:
        single_trainee.health_issue = True
        single_trainee.save()
        healthTrack = Health.objects.order_by('-injure').filter(trainee_id= single_trainee.id)
        if healthTrack:
            healthTrack = healthTrack[0]
            if healthTrack.recover:
                healthTrack = Health(trainee_id= single_trainee.id ,injure=now)
                healthTrack.save()
            else:
                healthTrack.recover = now
                healthTrack.save()
        else:
            healthTrack = Health(trainee_id= single_trainee.id ,injure=now)
            healthTrack.save()
    else:
        single_trainee.health_issue = False
        single_trainee.save()
        healthTrack = Health.objects.order_by('-injure').filter(trainee_id= single_trainee.id)
        if healthTrack:
            healthTrack = healthTrack[0]
            if not healthTrack.recover:
                healthTrack.recover = now
                healthTrack.save()
     

    issues_list = Trainees_health_issues.objects.filter(trainee__name=name).filter(
        healed=False).values_list('issue__code', flat=True).order_by('issue_date')
    solutions = Solution_list.objects.all().filter(
        issue__code__in=issues_list).filter(is_valid=True)

    trainee_shape = Shape_state.objects.order_by(
        '-date').filter(trainee__name=name)
    

    
    #! Experements
    # now = datetime.now(timezone.utc)
    # role = single_trainee.roll_date
    # c = now - role
    # print(now)
    # print(role)
    # print(c)
    #!###
    workout = Workouts.objects.order_by(
        '-date').filter(trainee__name=name)
    if workout:
        workout = workout[0]
    else:
        workout = None

    physiques = Physical_attribute.objects.order_by(
        '-date').filter(trainee__name=name)
    if physiques:
        physiques = physiques[0]

        # classifier
        if single_trainee:
            push_up = physiques.push_ups
            pull_up = physiques.pull_ups
            run = physiques.run

            pushup_score = pushup_result(push_up)
            pullup_score = pullup_result(pull_up)
            run_score = run_result(run)

            total_score = pushup_score + pullup_score + run_score
            score_level = total_score_level(total_score)
            #! shape State
            if trainee_shape:
                trainee_shape = trainee_shape[0]
                previous_level = trainee_shape.previous_level
                class_level = score_level
                class_shape = classifier_shape(
                    previous_level, class_level)
                if class_shape:
                    single_trainee.shape = True
                    single_trainee.save()
                    
                else:
                    single_trainee.shape = False
                    single_trainee.save()
                    
                    

            # back To classifier
            single_trainee.level = score_level
            single_trainee.save()
    else:
        single_trainee.level = 'beginner'
        single_trainee.save()

    # trainee_issues = Trainees_health_issues.objects.all().filter(trainee__id=trainee_id)
    issuesList = Issues.objects.all()
    context = {
        'single_trainee': single_trainee,
        'issues': issues,
        'solutions': solutions,
        'physiques': physiques,
        'issues_list': issuesList,
        'workout': workout,
        'age':t_age,
    }
    return render(request, 'trainees/trainee.html', context)


def note(request):
    if request.method == "POST":
        trainee_id = request.POST['trainee_id']
        notes = request.POST['notes']
        if request.user.is_authenticated:
            trainer_email = request.user.email
            his_trainer = Trainees.objects.all().filter(
                id=trainee_id, trainer__email=trainer_email)

            if his_trainer:
                his_trainer.update(note=notes)
                messages.success(
                    request, 'Your Note has been ADDED')
                return redirect('/trainees/'+trainee_id)
            elif request.user.is_staff:
                trainee = Trainees.objects.all().filter(
                    id=trainee_id)
                trainee.update(note=notes)
                messages.success(
                    request, 'Your Note has been ADDED')
                return redirect('/trainees/'+trainee_id)
            else:
                messages.error(
                    request, 'You are NOT his Trainer')
                return redirect('/trainees/'+trainee_id)

        else:
            messages.error(
                request, 'You MUST login To Add notes')
            return redirect('/trainees/'+trainee_id)


def physical_attribute(request):
    if request.method == "POST":
        trainee_id = request.POST['trainee_id']
        push_ups = request.POST['push_ups']
        pull_ups = request.POST['pull_ups']
        dips = request.POST['dips']
        handstand = request.POST['handstand']
        muscle_up = request.POST['muscle_up']
        deadlifts = request.POST['deadlifts']
        squat = request.POST['squat']
        bench_press = request.POST['bench_press']
        run = request.POST['run']
        l_set = request.POST['l_set']
        # retrive trainee
        single_trainee = Trainees.objects.order_by(
            '-roll_date').filter(id=trainee_id)[0]
        name = single_trainee.name
        ###
        if request.user.is_authenticated:
            trainer_email = request.user.email
            his_trainer = Trainees.objects.all().filter(
                id=trainee_id, trainer__email=trainer_email)

            if his_trainer:
                physical_attribute = Physical_attribute(trainee_id=trainee_id, push_ups=push_ups, pull_ups=pull_ups, dips=dips, handstand=handstand,
                                                        muscle_up=muscle_up, deadlifts=deadlifts, squat=squat, bench_press=bench_press, run=run, l_set=l_set)
                physical_attribute.save()
                physiques = Physical_attribute.objects.order_by(
                    '-date').filter(trainee__id=trainee_id)
                if physiques:
                    physiques = physiques[0]
                    # classifier
                    if single_trainee:
                        push_up = physiques.push_ups
                        pull_up = physiques.pull_ups
                        run = physiques.run

                        pushup_score = pushup_result(push_up)
                        pullup_score = pullup_result(pull_up)
                        run_score = run_result(run)

                        total_score = pushup_score + pullup_score + run_score
                        score_level = total_score_level(total_score)
                        # shape State
                        previous_level = single_trainee.level
                        shape_state = Shape_state(
                            trainee_id=single_trainee.id, classifier_level=score_level, previous_level=previous_level)
                        shape_state.save()

                        trainee_shape_state = Shape_state.objects.order_by(
                            '-date').filter(trainee__name=name)[0]
                        classifierLevel = trainee_shape_state.classifier_level
                        perviousLevel = trainee_shape_state.previous_level
                        class_shape = classifier_shape(
                            perviousLevel, classifierLevel)
                        shapeCounter = ShapeData.objects.all().filter(trainee__name=name)
                        if class_shape:
                            
                            single_trainee.shape = True
                            single_trainee.save()#!
                            if shapeCounter:
                                shapeCounter = shapeCounter[0]
                                shapeCounter.classifier_counter = shapeCounter.classifier_counter + 1
                                shapeCounter.in_shape_counter = shapeCounter.in_shape_counter + 1
                                shapeCounter.save()
                            else:
                                shapeData = ShapeData(trainee_id=single_trainee.id, classifier_counter = 1, in_shape_counter=1)
                                shapeData.save()
                            
                        else:
                            
                            single_trainee.shape = False
                            single_trainee.save()
                            if shapeCounter:
                                shapeCounter = shapeCounter[0]
                                shapeCounter.classifier_counter = shapeCounter.classifier_counter + 1
                                shapeCounter.out_shape_counter = shapeCounter.out_shape_counter + 1
                                shapeCounter.save()
                            else:
                                shapeData = ShapeData(trainee_id=single_trainee.id, classifier_counter = 1, out_shape_counter=1)
                                shapeData.save()

                messages.success(
                    request, 'Your Submition has been ADDED')

                return redirect('/trainees/'+trainee_id)

            elif request.user.is_staff:
                physical_attribute = Physical_attribute(trainee_id=trainee_id, push_ups=push_ups, pull_ups=pull_ups, dips=dips, handstand=handstand,
                                                        muscle_up=muscle_up, deadlifts=deadlifts, squat=squat, bench_press=bench_press, run=run, l_set=l_set)
                physical_attribute.save()
                physiques = Physical_attribute.objects.order_by(
                    '-date').filter(trainee__id=trainee_id)
                if physiques:
                    physiques = physiques[0]
                    # classifier
                    if single_trainee:
                        push_up = physiques.push_ups
                        pull_up = physiques.pull_ups
                        run = physiques.run

                        pushup_score = pushup_result(push_up)
                        pullup_score = pullup_result(pull_up)
                        run_score = run_result(run)

                        total_score = pushup_score + pullup_score + run_score
                        score_level = total_score_level(total_score)
                        # shape State
                        previous_level = single_trainee.level
                        shape_state = Shape_state(
                            trainee_id=single_trainee.id, classifier_level=score_level, previous_level=previous_level)           
                        shape_state.save()

                        trainee_shape_state = Shape_state.objects.order_by(
                            '-date').filter(trainee__name=name)[0]
                        classifierLevel = trainee_shape_state.classifier_level
                        if classifierLevel == 'advanced':
                            progress = Progress.objects.all().filter(trainee_id=trainee_id)
                            if not progress :
                                progress = Progress(trainee_id=trainee_id, level='advanced')
                                progress.save()
                        perviousLevel = trainee_shape_state.previous_level
                        class_shape = classifier_shape(
                            perviousLevel, classifierLevel)
                        shapeCounter = ShapeData.objects.all().filter(trainee__name=name)                           

                        if class_shape:
                            print('inside shape class')
                            single_trainee.shape = True
                            single_trainee.save()#!
                            if shapeCounter:
                                shapeCounter = shapeCounter[0]
                                shapeCounter.classifier_counter = shapeCounter.classifier_counter + 1
                                shapeCounter.in_shape_counter = shapeCounter.in_shape_counter + 1
                                shapeCounter.save()
                            else:
                                shapeData = ShapeData(trainee_id=single_trainee.id, classifier_counter = 1, in_shape_counter=1)
                                shapeData.save()
                        else:
                            single_trainee.shape = False
                            single_trainee.save()
                            if shapeCounter:
                                shapeCounter = shapeCounter[0]
                                shapeCounter.classifier_counter = shapeCounter.classifier_counter + 1
                                shapeCounter.out_shape_counter = shapeCounter.out_shape_counter + 1
                                shapeCounter.save()
                            else:
                                shapeData = ShapeData(trainee_id=single_trainee.id, classifier_counter = 1, out_shape_counter=1)
                                shapeData.save()

                messages.success(
                    request, 'Your Submition has been ADDED')
                return redirect('/trainees/'+trainee_id)

            else:
                messages.error(
                    request, 'You are NOT his Trainer')
                return redirect('/trainees/'+trainee_id)
        else:
            messages.error(
                request, 'You MUST login To Update Physical Attributes')
            return redirect('/trainees/'+trainee_id)


@login_required
def search(request):
    queryset_list = Trainees.objects.order_by('-trainer')

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(note__icontains=keywords)

    if 'trainer' in request.GET:
        trainer = request.GET['trainer']
        if trainer:
            queryset_list = queryset_list.filter(
                trainer__name__icontains=trainer)

    if 'health' in request.GET:
        health = request.GET['health']
        if health:
            if health == 'Yes':
                queryset_list = queryset_list.filter(health_issue=True)
            elif health == 'No':
                queryset_list = queryset_list.filter(health_issue=False)

    if 'level' in request.GET:
        level = request.GET['level']
        if level:
            queryset_list = queryset_list.filter(level=level)

    if 'elite' in request.GET:
        elite = request.GET['elite']
        if elite == 'Yes':
            queryset_list = queryset_list.filter(future_elite=True)
        elif elite == 'No':
            queryset_list = queryset_list.filter(future_elite=False)

    if 'shape' in request.GET:
        shape = request.GET['shape']
        if shape:
            if shape == 'Yes':
                queryset_list = queryset_list.filter(shape=True)
            elif shape == 'No':
                queryset_list = queryset_list.filter(shape=False)

    context = {
        'trainees_list': queryset_list,
        'values': request.GET,
    }
    return render(request, 'trainees/search.html', context)


def trainee_issue(request):
    if request.method == "POST":
        trainee_id = request.POST['trainee_id']
        issue = request.POST['issue']
        if request.user.is_authenticated:
            trainer_email = request.user.email
            his_trainer = Trainees.objects.all().filter(
                id=trainee_id, trainer__email=trainer_email)

            if his_trainer:
                new_issue = Trainees_health_issues(
                    trainee_id=trainee_id, issue_id=issue)
                new_issue.save()
                messages.success(
                    request, 'Trainee Issue Has Been ADDED')
                return redirect('/trainees/'+trainee_id)
            elif request.user.is_staff:
                new_issue = Trainees_health_issues(
                    trainee_id=trainee_id, issue_id=issue)
                new_issue.save()
                messages.success(
                    request, 'Trainee Issue Has Been ADDED')
                return redirect('/trainees/'+trainee_id)
            else:
                messages.error(
                    request, 'You are NOT his Trainer')
                return redirect('/trainees/'+trainee_id)

        else:
            messages.error(
                request, 'You MUST login To Add Trainee Issue')
            return redirect('/trainees/'+trainee_id)


def add_workout(request):
    if request.method == "POST":
        trainee_id = request.POST['trainee_id']
        content = request.POST['content']
        if request.user.is_authenticated:
            trainer_email = request.user.email
            trainer_id = request.user.id
            his_trainer = Trainees.objects.all().filter(
                id=trainee_id, trainer__email=trainer_email)

            if his_trainer:
                new_workout = Workouts(trainer_id=trainer_id,
                                       trainee__id=trainee_id, content=content)
                new_workout.save()
                messages.success(
                    request, 'Trainee Workout Has Been ADDED')
                return redirect('/trainees/'+trainee_id)
            elif request.user.is_staff:
                new_workout = Workouts(trainer_id=trainer_id,
                                       trainee_id=trainee_id, content=content)
                new_workout.save()
                messages.success(
                    request, 'Trainee Workout Has Been ADDED')
                return redirect('/trainees/'+trainee_id)
            else:
                messages.error(
                    request, 'You are NOT his Trainer')
                return redirect('/trainees/'+trainee_id)

        else:
            messages.error(
                request, 'You MUST login To Add Trainee Workout')
            return redirect('/trainees/'+trainee_id)


def edit_workout(request):
    if request.method == "POST":
        workout_id = request.POST['workout_id']
        content = request.POST['content']
        trainee_id = request.POST['trainee_id']
        if request.user.is_authenticated:
            trainer_email = request.user.email
            trainer_id = request.user.id
            his_trainer = Trainees.objects.all().filter(
                id=trainee_id, trainer__email=trainer_email)

            if his_trainer:
                workout = Workouts.objects.all().filter(id=workout_id)
                workout.update(content=content)

                messages.success(
                    request, 'Trainee Workout Has Been Edited')
                return redirect('/trainees/'+trainee_id)
            elif request.user.is_staff:
                workout = Workouts.objects.all().filter(id=workout_id)
                workout.update(content=content)

                messages.success(
                    request, 'Trainee Workout Has Been Edited')
                return redirect('/trainees/'+trainee_id)
            else:
                messages.error(
                    request, 'You are NOT his Trainer')
                return redirect('/trainees/'+trainee_id)
        else:
            messages.error(
                request, 'You MUST login To Add Trainee Workout')
            return redirect('/trainees/'+trainee_id)


def workouts_list(request, trainee_id):
    t_id = trainee_id
    workouts = Workouts.objects.order_by(
        '-date').filter(trainee__id=t_id)
    print(workouts)
    context = {
        'workouts': workouts,
    }
    return render(request, 'trainees/workouts_list.html', context)

def active(request):
    if request.method == "POST":
        now = datetime.now(timezone.utc)
        trainee_id = request.POST['trainee_id']
        single_trainee = get_object_or_404(Trainees, pk=trainee_id)
        active = str_to_bool(request.POST['active'])
        
        currentState = single_trainee.is_active

        if active:  
            traineeActivity = Activity.objects.order_by('-inactive').filter(trainee__id=trainee_id)
            if traineeActivity:
                traineeActivity = traineeActivity[0]
                if traineeActivity.active:
                    messages.error(request, 'Trainee already active')
                    return redirect('/trainees/'+trainee_id)
                else:
                    traineeActivity.active = now
                    traineeActivity.save()
                    single_trainee.is_active = True
                    single_trainee.save()
                    messages.success(
                    request, 'Trainee status been updated')
                    return redirect('/trainees/'+trainee_id)
            else:
                messages.error(request, 'Trainee already active')
                return redirect('/trainees/'+trainee_id)
        else:
            if currentState:
                inactivePeriod = Activity(trainee_id = trainee_id, inactive=now)
                inactivePeriod.save()
                single_trainee.is_active = False
                single_trainee.save()
                messages.success(
                        request, 'Trainee status been updated')
                return redirect('/trainees/'+trainee_id)
            else:
                messages.error(request, 'Trainee already inactive')
                return redirect('/trainees/'+trainee_id)





        