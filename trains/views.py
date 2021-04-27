from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView, CreateView, UpdateView, DeleteView,
    ListView
)
from cities.models import City
from trains.forms import TrainForm, UploadTrainForm
from trains.models import Train
from django.shortcuts import redirect
import tablib

__all__ = (
    'home', 'TrainListView',
    'TrainDetailView',
    'TrainCreateView', 'TrainUpdateView',
    'TrainDeleteView',
)


def home(request, pk=None):
    qs = Train.objects.all()
    lst = Paginator(qs, 5)
    page_number = request.GET.get('page')
    page_obj = lst.get_page(page_number)
    context = {'page_obj': page_obj,}
    return render(request, 'trains/home.html', context)

def handle_train_import(raw_data):
    dataset = tablib.Dataset().load(raw_data)
    headers = [
        x.lower().replace(' ', '_') for x in dataset.headers if x is not None
    ]
    if len(headers) != 4:
        raise Exception('Invalid format to import cities')
    for row in dataset:
        name = row[0]
        travel_time = int(row[1])
        from_city = row[2]
        to_city = row[3]
        try:
            from_city = City.objects.get(name=from_city)
            to_city = City.objects.get(name=to_city)
        except:
            continue
        Train.objects.create(
            name=name,
            travel_time=travel_time,
            from_city=from_city,
            to_city=to_city
        )
        
    
    

def upload(request):
    if request.method == 'POST':
        form = UploadTrainForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                raw_data = request.FILES['file'].open('rb').read()
                handle_train_import(raw_data)
            except Exception as e:
                messages.error(request, f'{e}')
        
        return redirect(reverse_lazy('trains:home'))
    context = {'form': UploadTrainForm()}
    return render(request, 'trains/upload.html', context)


class TrainListView(ListView):
    paginate_by = 10
    model = Train
    template_name = 'trains/home.html'


class TrainDetailView(DetailView):
    queryset = Train.objects.all()
    template_name = 'trains/detail.html'


class TrainCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/create.html'
    success_url = reverse_lazy('trains:home')
    success_message = "Train successfully created"


class TrainUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/update.html'
    success_url = reverse_lazy('trains:home')
    success_message = "Train successfully updated"


class TrainDeleteView(LoginRequiredMixin, DeleteView):
    model = Train
    success_url = reverse_lazy('trains:home')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Train successfully deleted')
        return self.post(request, *args, **kwargs)