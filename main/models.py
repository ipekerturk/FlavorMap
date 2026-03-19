from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Location(models.Model):
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city} - {self.district}"


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    price_range = models.CharField(max_length=10)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def average_rating(self):
        reviews = self.review_set.all()
        if reviews.exists():
            return sum(r.rating for r in reviews) / reviews.count()
        return 0


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.rating}"
