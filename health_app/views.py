from django.shortcuts import render, get_object_or_404, redirect
from trainees.models import *
from health_app.models import *
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    # CreateView,
    DetailView,
    DeleteView,
    # ListView,
    # UpdateView,
    # ListView,

)


@login_required
def level(request):
    b_ath = Trainees.objects.all().filter(level='beginner')
    i_ath = Trainees.objects.all().filter(level='intermediate')
    a_ath = Trainees.objects.all().filter(level='advanced')
    e_ath = Trainees.objects.all().filter(level='elite')
    context = {
        'beginners': b_ath,
        'intermediates': i_ath,
        'advanceds': a_ath,
        'elites': e_ath,
    }
    return render(request, 'health_app/athletesLevel.html', context)


@login_required
def injured(request):
    injured_ath = Trainees.objects.all().filter(health_issue=True)
    context = {
        'injureds': injured_ath,
    }

    return render(request, 'health_app/injured.html', context)


@login_required
def shape(request):
    shape_ath = Trainees.objects.all().filter(shape=True)
    context = {
        'shapes': shape_ath,

    }
    return render(request, 'health_app/shape.html', context)


@login_required
def elite(request):
    elite_ath = Trainees.objects.all().filter(future_elite=True)
    context = {
        'elites': elite_ath,

    }
    return render(request, 'health_app/elite.html', context)


def health_list(request):
    h_list = Issues.objects.all().filter(solve_ability=True)
    context = {
        'health_list': h_list

    }
    return render(request, 'health_app/health_list.html', context)


def issue_search(request):

    if 'trainee' in request.GET:
        queryset_list = Trainees_health_issues.objects.order_by('-issue_date')
        trainee = request.GET['trainee']
        # solve url problem later
        if trainee:
            queryset_list = queryset_list.filter(
                trainee__name__icontains=trainee)
        else:
            queryset_list = Issues.objects.all()

    if 'code' in request.GET:
        code = request.GET['code']
        if code == '':
            queryset_list = queryset_list
        else:
            queryset_list = Issues.objects.all()
            queryset_list = queryset_list.filter(code__icontains=code)

    if 'description' in request.GET:
        description = request.GET['description']
        if description == '':
            queryset_list = queryset_list
        else:
            queryset_list = Issues.objects.all()
            queryset_list = queryset_list.filter(
                description__icontains=description)

    context = {
        'results': queryset_list,
        'values': request.GET,
    }
    return render(request, 'health_app/search.html', context)


# class IssueDetailView(DetailView):
#     queryset = Issues.objects.all()
#     template_name = 'health_app/issue.html'
#     # To overwrite pk <int:pk>

#     def get_object(self):
#         id_ = self.kwargs.get('id')
#         return get_object_or_404(Issues, id=id_)


def Issue_details(request, issue_id):
    single_issue = get_object_or_404(Issues, pk=issue_id)
    solutions = Solution_list.objects.all().filter(
        issue__code=single_issue).filter(is_valid=True)
    context = {
        'single_issue': single_issue,
        'solutions': solutions,
    }
    return render(request, 'health_app/issue.html', context)


class IssueDeleteView(DeleteView):
    template_name = 'health_app/issue_delete.html'
    queryset = Issues.objects.all()
    # To overwrite pk <int:pk>

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Issues, id=id_)

    def get_success_url(self):
        return reverse('health_app:list')


def update_issue(request):
    if request.method == "POST":
        obj_id = request.POST['issue_id']
        description = request.POST['description']
        issue = Issues.objects.all().filter(id=obj_id)
        issue.update(description=description)
        messages.success(
            request, 'Your Submition has been ADDED')
        return redirect('/health/'+obj_id)


class TraineeIssueDetailView(DetailView):
    queryset = Trainees_health_issues.objects.all()
    template_name = 'health_app/trainee_issue_details.html'
    # To overwrite pk <int:pk>

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Trainees_health_issues, id=id_)


class TraineeIssueDeleteView(DeleteView):
    template_name = 'health_app/trainee_issue_delete.html'
    queryset = Trainees_health_issues.objects.all()
    # To overwrite pk <int:pk>

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Trainees_health_issues, id=id_)

    def get_success_url(self):
        return reverse('health_app:list')


def healed_update(request):
    if request.method == "POST":
        obj_id = request.POST['id']
        healed = request.POST['healed']
        trainee_id = request.POST['traineeid']

        issue = Trainees_health_issues.objects.all().filter(id=obj_id)
        if healed == 'Yes':
            issue.update(healed=True)
        messages.success(
            request, 'Your Submition has been ADDED')
        return redirect('/trainees/'+trainee_id)
