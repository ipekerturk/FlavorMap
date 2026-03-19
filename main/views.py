from django.shortcuts import render, get_object_or_404
from .models import Restaurant, Review, Category, Location


def home(request):
    return render(request, 'home.html')


def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    categories = Category.objects.all()
    locations = Location.objects.all()

    context = {
        'restaurants': restaurants,
        'categories': categories,
        'locations': locations,
    }

    return render(request, 'restaurant_list.html', context)


def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    reviews = Review.objects.filter(restaurant=restaurant)

    context = {
        'restaurant': restaurant,
        'reviews': reviews,
    }

    return render(request, 'restaurant_detail.html', context)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')