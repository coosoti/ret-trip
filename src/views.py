from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def customer_page(request):
    return render(request, 'index.html')

def driver_page(request):
    return render(request, 'index.html')
