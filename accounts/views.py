from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from trainees.models import Trainees
from trainers.models import Trainer
from django.contrib.auth.decorators import login_required
from health_app.models import *


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            trainees_list = Trainees.objects.order_by(
                '-trainer').filter(is_active=True)
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')


@login_required
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'you are now logged out')
        return redirect('index')


@login_required
def dashboard(request):
    queryset_list = Trainees.objects.order_by(
        '-roll_date').filter(trainer__email=request.user.email)

    health_list = Trainees.objects.order_by(
        '-roll_date').filter(health_issue=True, trainer__email=request.user.email)

    shape_list = Trainees.objects.order_by(
        '-roll_date').filter(shape=True, trainer__email=request.user.email)

    elite_list = Trainees.objects.order_by(
        '-roll_date').filter(future_elite=True, trainer__email=request.user.email)

    # select issues and solutions
    issues_list = Issues.objects.all()
    sol_list = Solutions.objects.all()

    # counters
    total_athlete = queryset_list.count()
    shape_count = shape_list.count()
    health_count = health_list.count()
    elite_count = elite_list.count()

    context = {
        'trainer_clients': queryset_list,
        'health_list': health_list,
        'shape_list': shape_list,
        'elite_list': elite_list,
        'shape_count': shape_count,
        'total_athlete': total_athlete,
        'health_count': health_count,
        'elite_count': elite_count,
        'issues_list': issues_list,
        'sol_list': sol_list,
    }

    return render(request, 'accounts/dashboard.html', context)


def add_issue(request):
    if request.method == "POST":
        code = request.POST['code']
        description = request.POST['description']
        if request.user.is_authenticated:
            issue = Issues(code=code, description=description)
            issue.save()
            messages.success(
                request, 'Issue has been ADDED')
            return redirect('dashboard')
        else:
            messages.error(
                request, 'You MUST login To Add Issues')
            return redirect('dashboard')


def add_sol(request):
    if request.method == "POST":
        code = request.POST['code']
        description = request.POST['description']
        if request.user.is_authenticated:
            sol = Solutions(code=code, description=description)
            sol.save()
            messages.success(
                request, 'Solution has been ADDED')
            return redirect('dashboard')
        else:
            messages.error(
                request, 'You MUST login To Add Solution')
            return redirect('dashboard')


def add_list(request):
    if request.method == "POST":
        issue = request.POST['issue']
        solution = request.POST['solution']
        if request.user.is_authenticated:
            sol_list = Solution_list(issue_id=issue, solution_id=solution)
            sol_list.save()
            messages.success(
                request, 'Solution List has been ADDED')
            return redirect('dashboard')
        else:
            messages.error(
                request, 'You MUST login To Add Solution List')
            return redirect('dashboard')
