from django.shortcuts import render

def home(request):
    name = 'Akarys'
    return render(request, 'home.html', {'name':name})
    