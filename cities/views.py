from django.shortcuts import render
from .models import City
# Create your views here.

def home(request):
    qs = City.objects.all()
    context = {'objects_list':qs}
    return render(request, 'citites/home.html', context)