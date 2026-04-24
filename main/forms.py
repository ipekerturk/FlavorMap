from django import forms
from django.contrib.auth.models import User
from .models import Restaurant, Review



class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Şifre'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kullanıcı Adı'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-posta'}),
        }



class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant

        fields = ['name', 'category', 'location', 'description', 'price_range', 'address', 'phone', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price_range': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {

            'rating': forms.Select(choices=[(i, f"{i} Yıldız") for i in range(1, 6)], attrs={'class': 'form-control'}),
            'comment': forms.Textarea(
                attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Yorumunuzu buraya yazın...'}),
        }