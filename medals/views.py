from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView, CreateView

from .models import Medal, Soldier


class MedalsList(LoginRequiredMixin, ListView):
    paginate_by = 15
    model = Medal
    login_url = 'login'


@login_required(login_url='/login')
def SearchMedal(request):
    template_name = 'medals/search_medal.html'
    soldiers = Soldier.objects.all()
    medals = Medal.objects.all()
    if request.method == 'POST':
        pass
        '''
        form = CarrierForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            if form.is_valid():
                form.save()
                return redirect('home')
            else:
                form = CarrierForm(request.POST, request.FILES)'''
    return render(request, template_name, {'soldiers': soldiers, 'medals': medals})
