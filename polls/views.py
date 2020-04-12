from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(requesrt):
    return HttpResponse("my own website xddd")