from django.shortcuts import render
from .models import AdmMapa

# Create your views here.
def index(request):
    #return render(request, 'index.html')
    shp = AdmMapa.objects.all()
    return render(request, 'index.html',{'shp':shp})
