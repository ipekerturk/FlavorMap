from django import forms
from .models import Restaurant, Review

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant

        fields = ['name', 'category', 'location', 'description', 'image']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review

        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }