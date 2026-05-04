from django.contrib import admin
from .models import Category, Location, Restaurant, Review, MenuItem, Favorite


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'location',
        'price_range',
        'opening_hours',
        'owner',
    )

    fields = (
        'owner',
        'name',
        'description',
        'address',
        'phone',
        'price_range',
        'category',
        'location',
        'image',
        'opening_hours',
    )

    search_fields = ('name', 'description', 'address')
    list_filter = ('category', 'location', 'price_range')
    inlines = [MenuItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price', 'category')
    search_fields = ('name', 'description', 'restaurant__name')
    list_filter = ('restaurant', 'category')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'user', 'rating', 'created_at', 'parent')
    search_fields = ('comment', 'restaurant__name', 'user__username')
    list_filter = ('rating', 'created_at')


admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Favorite)