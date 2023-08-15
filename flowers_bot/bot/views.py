from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return HttpResponse('<h1>Сервис <span style="color:red">FlowerShop!</span></h1>')