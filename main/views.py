from django.shortcuts import render, get_object_or_404
from .models import Restaurant


def home(request):
    return render(request, 'home.html')


def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurant_list.html', {'restaurants': restaurants})


def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    return render(request, 'restaurant_detail.html', {'restaurant': restaurant})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')