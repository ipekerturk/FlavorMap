from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, Review, Category, Location, Favorite, MenuItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import RestaurantForm, ReviewForm
from django.db.models import Q, Avg
from django.db import transaction, IntegrityError


def restaurant_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    location_id = request.GET.get('location', '')
    price_range = request.GET.get('price_range', '')

    restaurants = Restaurant.objects.all()
    categories = Category.objects.all()
    locations = Location.objects.all()

    if query:
        restaurants = restaurants.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(location__city__icontains=query) |
            Q(location__district__icontains=query)
        )

    if category_id:
        restaurants = restaurants.filter(category_id=category_id)
        category_id = int(category_id)

    if location_id:
        restaurants = restaurants.filter(location_id=location_id)
        location_id = int(location_id)

    if price_range:
        restaurants = restaurants.filter(price_range=price_range)

    context = {
        'restaurants': restaurants,
        'categories': categories,
        'locations': locations,
        'query': query,
        'category_id': category_id,
        'location_id': location_id,
        'price_range': price_range,
        'price_choices': Restaurant.PRICE_CHOICES,
    }

    return render(request, 'restaurant_list.html', context)


def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    reviews = Review.objects.filter(restaurant=restaurant, parent__isnull=True)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)

    user_review_exists = False
    is_favorite = False
    is_owner = False
    error_message = None

    if request.user.is_authenticated:
        user_review_exists = Review.objects.filter(
            restaurant=restaurant,
            user=request.user,
            parent__isnull=True
        ).exists()

        is_favorite = Favorite.objects.filter(
            restaurant=restaurant,
            user=request.user
        ).exists()

        is_owner = restaurant.owner == request.user

    if request.method == "POST" and request.user.is_authenticated and not user_review_exists:
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            try:
                with transaction.atomic():
                    review = review_form.save(commit=False)
                    review.restaurant = restaurant
                    review.user = request.user
                    review.save()

                return redirect('restaurant_detail', id=restaurant.id)

            except IntegrityError:
                error_message = "An error occurred while saving your review. Please try again."
    else:
        review_form = ReviewForm()

    context = {
        'restaurant': restaurant,
        'reviews': reviews,
        'review_form': review_form,
        'menu_items': menu_items,
        'user_review_exists': user_review_exists,
        'is_favorite': is_favorite,
        'is_owner': is_owner,
        'error_message': error_message,
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
            try:
                with transaction.atomic():
                    form.save()

                return redirect('login')

            except IntegrityError:
                return render(request, 'register.html', {
                    'form': form,
                    'error_message': 'An error occurred while creating your account.'
                })
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def restaurant_create(request):
    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                with transaction.atomic():
                    restaurant = form.save(commit=False)
                    restaurant.owner = request.user
                    restaurant.save()

                return redirect('restaurant_detail', id=restaurant.id)

            except IntegrityError:
                return render(request, 'restaurant_form.html', {
                    'form': form,
                    'title': 'Add Restaurant',
                    'error_message': 'An error occurred while creating the restaurant.'
                })
    else:
        form = RestaurantForm()

    return render(request, 'restaurant_form.html', {
        'form': form,
        'title': 'Add Restaurant'
    })


@login_required
def toggle_favorite(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)

    try:
        with transaction.atomic():
            favorite, created = Favorite.objects.get_or_create(
                user=request.user,
                restaurant=restaurant
            )

            if not created:
                favorite.delete()

    except IntegrityError:
        pass

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
        try:
            with transaction.atomic():
                already_reviewed = Review.objects.filter(
                    restaurant=restaurant,
                    user=request.user,
                    parent__isnull=True
                ).exists()

                if not already_reviewed:
                    comment = request.POST.get('comment')
                    rating = request.POST.get('rating')

                    Review.objects.create(
                        restaurant=restaurant,
                        user=request.user,
                        comment=comment,
                        rating=rating
                    )

        except IntegrityError:
            pass

    return redirect('restaurant_detail', id=restaurant_id)


@login_required
def add_review_reply(request, review_id):
    parent_review = get_object_or_404(Review, id=review_id)

    if request.method == 'POST':
        comment = request.POST.get('comment')

        if comment:
            try:
                with transaction.atomic():
                    Review.objects.create(
                        restaurant=parent_review.restaurant,
                        user=request.user,
                        comment=comment,
                        rating=5,
                        parent=parent_review
                    )

            except IntegrityError:
                pass

    return redirect('restaurant_detail', id=parent_review.restaurant.id)


@login_required
def review_edit(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()

                return redirect('restaurant_detail', id=review.restaurant.id)

            except IntegrityError:
                return render(request, 'review_form.html', {
                    'form': form,
                    'title': 'Edit Review',
                    'error_message': 'An error occurred while updating the review.'
                })
    else:
        form = ReviewForm(instance=review)

    return render(request, 'review_form.html', {
        'form': form,
        'title': 'Edit Review'
    })


@login_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    restaurant_id = review.restaurant.id

    if request.method == "POST":
        try:
            with transaction.atomic():
                review.delete()

            return redirect('restaurant_detail', id=restaurant_id)

        except IntegrityError:
            return render(request, 'review_confirm_delete.html', {
                'review': review,
                'error_message': 'An error occurred while deleting the review.'
            })

    return render(request, 'review_confirm_delete.html', {
        'review': review
    })


@login_required
def restaurant_edit(request, id):
    restaurant = get_object_or_404(Restaurant, id=id, owner=request.user)

    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)

        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()

                return redirect('restaurant_detail', id=restaurant.id)

            except IntegrityError:
                return render(request, 'restaurant_form.html', {
                    'form': form,
                    'title': 'Edit Restaurant',
                    'error_message': 'An error occurred while updating the restaurant.'
                })
    else:
        form = RestaurantForm(instance=restaurant)

    return render(request, 'restaurant_form.html', {
        'form': form,
        'title': 'Edit Restaurant'
    })


@login_required
def restaurant_delete(request, id):
    restaurant = get_object_or_404(Restaurant, id=id, owner=request.user)

    if request.method == "POST":
        try:
            with transaction.atomic():
                restaurant.delete()

            return redirect('restaurant_list')

        except IntegrityError:
            return render(request, 'restaurant_confirm_delete.html', {
                'restaurant': restaurant,
                'error_message': 'An error occurred while deleting the restaurant.'
            })

    return render(request, 'restaurant_confirm_delete.html', {
        'restaurant': restaurant
    })
# 🔥 MENU CREATE
@login_required
def menu_create(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, owner=request.user)

    if request.method == "POST":
        form = MenuItemForm(request.POST)

        if form.is_valid():
            item = form.save(commit=False)
            item.restaurant = restaurant
            item.save()

            return redirect('restaurant_detail', id=restaurant.id)
    else:
        form = MenuItemForm()

    return render(request, 'menu_item_form.html', {
        'form': form,
        'title': 'Add Menu Item'
    })


# 🔥 MENU EDIT
@login_required
def menu_edit(request, id):
    item = get_object_or_404(MenuItem, id=id, restaurant__owner=request.user)

    if request.method == "POST":
        form = MenuItemForm(request.POST, instance=item)

        if form.is_valid():
            form.save()
            return redirect('restaurant_detail', id=item.restaurant.id)
    else:
        form = MenuItemForm(instance=item)

    return render(request, 'menu_item_form.html', {
        'form': form,
        'title': 'Edit Menu Item'
    })


# 🔥 MENU DELETE
@login_required
def menu_delete(request, id):
    item = get_object_or_404(MenuItem, id=id, restaurant__owner=request.user)
    restaurant_id = item.restaurant.id

    if request.method == "POST":
        item.delete()
        return redirect('restaurant_detail', id=restaurant_id)

    return render(request, 'menu_item_confirm_delete.html', {
        'item': item
    })