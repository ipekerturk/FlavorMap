from django.contrib import admin
from .models import Category, Location, Restaurant, Review

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'location', 'price_range')
    search_fields = ('name', 'description')
    list_filter = ('category', 'location')

admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Review)