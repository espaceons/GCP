from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def fca(request):
    context = {}
    return render(request, 'FCA.html', context)
