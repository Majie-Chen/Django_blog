from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

def home(request):
    context = {}
    return render(request, 'myhome.html', context)