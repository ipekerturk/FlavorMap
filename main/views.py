from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, Review, Category, Location, Favorite, MenuItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import RestaurantForm, ReviewForm
from django.db.models import Q




def restaurant_list(request):
    # Kullanıcının arama ve filtreleme kelimelerini alıyoruz (URL'den GET ile)
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')

    # Önce tüm restoranları ve kategorileri veritabanından çekiyoruz
    restaurants = Restaurant.objects.all()
    categories = Category.objects.all()

    # Eğer arama kutusuna bir şey yazılmışsa, isminde o kelime geçenleri filtrele (icontains: büyük/küçük harf duyarsız arama yapar)
    if query:
        restaurants = restaurants.filter(name__icontains=query)

    # Eğer dropdown'dan bir kategori seçilmişse, sadece o kategoriye ait olanları getir
    if category_id:
        restaurants = restaurants.filter(category_id=category_id)
        category_id = int(category_id)  # HTML'de seçili kalması için sayıya çeviriyoruz

    context = {
        'restaurants': restaurants,
        'categories': categories,
        'query': query,
        'category_id': category_id,
    }

    return render(request, 'restaurant_list.html', context)


def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    reviews = Review.objects.filter(restaurant=restaurant)
    if request.method == "POST" and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.restaurant = restaurant
            review.user = request.user
            review.save()
            return redirect('restaurant_detail', id=restaurant.id)
    else:
        review_form = ReviewForm()
    context = {
        'restaurant': restaurant,
        'reviews': reviews,
        'review_form': review_form,
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


@login_required
def toggle_favorite(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)

    favorite, created = Favorite.objects.get_or_create(user=request.user, restaurant=restaurant)

    if not created:
        favorite.delete()

    return redirect('restaurant_detail', id=id)


@login_required
def user_profile(request):

    user_favorites = Favorite.objects.filter(user=request.user)

    user_reviews = Review.objects.filter(user=request.user)

    context = {
        'favorites': user_favorites,
        'reviews': user_reviews,
    }
    return render(request, 'profile.html', context)


from django.db.models import Avg


from django.db.models import Avg # 1. Bunu en üste eklemeyi unutma!

from django.db.models import Avg # Dosyanın en üstünde olduğundan emin ol!

def home(request):

    newest = Restaurant.objects.order_by('-id')[:3]
    top_rated = Restaurant.objects.annotate(
        avg_score=Avg('reviews__rating')
    ).order_by('-avg_score')[:3]


    context = {
        'newest': newest,
        'top_rated': top_rated,
        'popular_restaurants': top_rated
    }


    return render(request, 'home.html', context)


@login_required
def add_review(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == 'POST':
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')

        Review.objects.create(
            restaurant=restaurant,
            user=request.user,
            comment=comment,
            rating=rating
        )
    return redirect('restaurant_detail', id=restaurant_id)


@login_required
def add_review_reply(request, review_id):
    parent_review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        comment = request.POST.get('comment')


        Review.objects.create(
            restaurant=parent_review.restaurant,
            user=request.user,
            comment=comment,
            rating=5,
            parent=parent_review
        )
    return redirect('restaurant_detail', id=parent_review.restaurant.id)

@login_required
def restaurant_edit(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)

    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('restaurant_detail', id=restaurant.id)
    else:
        form = RestaurantForm(instance=restaurant)

    return render(request, 'restaurant_form.html', {
        'form': form,
        'title': 'Edit Restaurant'
    })


@login_required
def restaurant_delete(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)

    if request.method == "POST":
        restaurant.delete()
        return redirect('restaurant_list')

    return render(request, 'restaurant_confirm_delete.html', {
        'restaurant': restaurant
    })