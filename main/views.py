from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')


def restaurant_list(request):
    restaurants = [
        {'id': 1, 'name': 'Pizza Place', 'rating': 4.5},
        {'id': 2, 'name': 'Sushi Bar', 'rating': 4.8},
    ]
    return render(request, 'restaurant_list.html', {'restaurants': restaurants})


def restaurant_detail(request, id):
    restaurant = {
        'id': id,
        'name': 'Pizza Place',
        'description': 'Best pizza in town',
        'rating': 4.5
    }
    return render(request, 'restaurant_detail.html', {'restaurant': restaurant})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')