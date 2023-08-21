from django.shortcuts import render
from django.http import HttpResponse
from .models import Catalog

# Create your views here.
def index(request):
	Catalog.get_catalog()
	print('-=-=-=-=-=-=-=-=-')
	Catalog.get_bouquet(3, 'Не важно')
	return HttpResponse('<h1>Сервис <span style="color:red">FlowerShop!</span></h1>')