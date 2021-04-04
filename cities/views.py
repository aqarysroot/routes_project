from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, \
    ListView

from cities.forms import HtmlForm, CityForm, UploadForm
from cities.models import City
from rest_framework.views import APIView
from django.shortcuts import redirect
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError



__all__ = (
    'home', 'CityDetailView', 'CityCreateView', 'CityUpdateView',
    'CityDeleteView', 'CityListView', 'upload',
)

# class ParseExcel(APIView):
#     template_name = 'cities/upload.html'
#     form_class = UploadForm
#     def post(self, request, format=None):
#         try:
#             excel_file = request.FILES['files']
#         except MultiValueDictKeyError:
#             return redirect('')
#         if (str(excel_file).split('.')[-1] == 'xls'):
#             data = xls_get(excel_file, column_limit=4)
#         elif (str(excel_file).split('.')[-1] == 'xlsx'):
#             data = xlsx_get(excel_file, column_limit=4)
#         else:
#             return redirect('')

def upload(request):
    form = UploadForm(request.POST, request.FILES)
    if request.method == 'POST':
        try:
            myfile = request.FILES['file']
        except MultiValueDictKeyError:
            return redirect(reverse_lazy('cities:home'))
        if str(myfile).split('.')[-1] == 'xls':
            data = xls_get(myfile, column_limit=2)
        elif str(myfile).split('.')[-1] == 'xlsl':
            data = xlsx_get(myfile, column_limit=2)
        cities = data['citites']
        for city in cities:
            if len(city) > 0:
                if city[0] != 'No':
                    name = city[1]
                    City.objects.create(name=name)

        
        return redirect(reverse_lazy('cities:home'))
    context = {'form': UploadForm()}
    return render(request, 'cities/upload.html', context)
    
            
    


def home(request, pk=None):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
    form = CityForm()
    qs = City.objects.all()
    lst = Paginator(qs, 2)
    page_number = request.GET.get('page')
    page_obj = lst.get_page(page_number)
    context = {'page_obj': page_obj, 'form': form}
    return render(request, 'cities/home.html', context)


class CityDetailView(DetailView):
    queryset = City.objects.all()
    template_name = 'cities/detail.html'


class CityCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = City
    form_class = CityForm
    template_name = 'cities/create.html'
    success_url = reverse_lazy('cities:home')
    success_message = "City was created"


class CityUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/update.html'
    success_url = reverse_lazy('cities:home')
    success_message = "City was updated"


class CityDeleteView(LoginRequiredMixin, DeleteView):
    model = City
    success_url = reverse_lazy('cities:home')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'City was deleted')
        return self.post(request, *args, **kwargs)


class CityListView(ListView):
    paginate_by = 10
    model = City
    template_name = 'cities/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CityForm()
        context['form'] = form
        return context