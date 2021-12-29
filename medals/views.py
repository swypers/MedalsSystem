from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.views.generic.detail import DetailView

from .models import Medal, Soldier, Photos, Merits, GivenMedals
from .forms import GivenMedalsForm


class MedalsList(LoginRequiredMixin, ListView):
    paginate_by = 15
    model = Medal
    login_url = 'login'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['photos'] = Photos.objects.all()
        return context


class MedalDetailView(LoginRequiredMixin, DetailView):
    queryset = Medal.objects.all()
    context_object_name = 'object'
    template_name = 'medals/medal_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['photos'] = Photos.objects.filter(medal__pk=self.kwargs['pk'])
        return context


@login_required(login_url='/login')
class GivenMedalCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):  # class создания нового города
    model = GivenMedals  # model
    form_class = GivenMedalsForm  # class privyazki
    login_url = 'login'
    template_name = 'medals/medal_give.html'
    success_url = reverse_lazy(
        'home')  # Страница, на которую мы вернёмся после нажатия кнопки submit в случае успеха
    success_message = 'Медаль успешно выдана военнослужащему'

    def get_initial(self):
        pk = self.request.POST.get('pk')
        medal_pk = self.request.POST.get('medal_pk')
        return {'soldier': pk, 'medals': pk}



@login_required(login_url='/login')
def SearchMedal(request):
    context = dict()
    template_name = 'medals/search_medal.html'
    soldiers = Soldier.objects.all()
    medals = Medal.objects.all()
    merits = Merits.objects.all()
    context['soldiers'] = soldiers
    context['medals'] = medals
    context['merits'] = merits
    context['photos'] = Photos.objects.all()
    if request.method == 'POST':
        query = request.POST.get('query')
        soldier_pk = request.POST.get('soldier')
        context['chosen_soldier'] = soldier_pk
        context['query'] = query
        print(query)
        print(soldier_pk)
        print('post')
        raw_query = """SELECT id,name, ts_rank_cd(searchvec, query, 32 /* rank/(rank+1) */ ) AS rank,
                        ts_headline('russian',rules,
                                    websearch_to_tsquery('{query}'),
                                    'HighlightAll=false,MaxWords=100,StartSel=<mark>,StopSel=</mark>') as hl 
                        FROM medals_medal, websearch_to_tsquery('russian','{query}') query 
                        WHERE  query @@ searchvec 
                        ORDER BY rank DESC""".format(query=query)
        print(raw_query)
        objects_list = Medal.objects.raw(raw_query)
        print(objects_list)
        context['objects_list'] = objects_list
    return render(request, template_name, context)
