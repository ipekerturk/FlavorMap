from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('restaurants/create/', views.restaurant_create, name='restaurant_create'),
    path('restaurants/<int:id>/', views.restaurant_detail, name='restaurant_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),


    path('profile/', views.user_profile, name='user_profile'),
    path('restaurant/<int:id>/favorite/', views.toggle_favorite, name='toggle_favorite'),


    path('restaurant/<int:restaurant_id>/add_review/', views.add_review, name='add_review'),
    path('review/<int:review_id>/reply/', views.add_review_reply, name='add_review_reply'),
]