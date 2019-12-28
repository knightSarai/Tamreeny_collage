from django.shortcuts import render
from trainers.models import Trainer
from trainees.models import Trainees
from django.contrib.auth.decorators import login_required


def index(request):
    latest_trainee = Trainees.objects.order_by(
        '-roll_date').filter(is_active=True)[:3]

    all_trainees = Trainees.objects.all()
    all_trainees_count = all_trainees.count()
    Injured_trainee = all_trainees.filter(health_issue=True).count()
    shape_trainees = all_trainees.filter(shape=True).count()
    b_trainees = all_trainees.filter(level='beginner').count()
    i_trainees = all_trainees.filter(level='intermediate').count()
    a_trainees = all_trainees.filter(level='advanced').count()
    e_trainees = all_trainees.filter(level='elite').count()
    future_elite = all_trainees.filter(future_elite=True).count()
    elite_trainees = future_elite - e_trainees
    context = {
        'latest_trainee': latest_trainee,
        'all_trainees_count': all_trainees_count,
        'Injured_trainee': Injured_trainee,
        'shape_trainees': shape_trainees,
        'elite_trainees': elite_trainees,
        'b_trainees': b_trainees,
        'i_trainees': i_trainees,
        'a_trainees': a_trainees,
        'e_trainees': e_trainees,
    }
    return render(request, 'pages/index.html', context)


@login_required
def gym(request):
    trainers_list = Trainer.objects.order_by('-hire_date')
    mvp_list = Trainer.objects.all().filter(is_mvp=True)
    context = {
        'trainers_list': trainers_list,
        'mvp_list': mvp_list
    }
    return render(request, 'pages/gym.html', context)
