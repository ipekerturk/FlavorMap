from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, Review, Category, Location
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import RestaurantForm, ReviewForm
from django.db.models import Q

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


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def restaurant_create(request):
    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save()
            restaurant.save()
            return redirect('restaurant_list')
    else:
        form = RestaurantForm()
    return render(request, 'restaurant_form.html', {'form': form, 'title': 'Add Restaurant'})

