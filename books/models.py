from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='books/')

    # 💰 NEW FIELDS
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title

    # 🔥 Optional helper: check if discount exists
    def has_discount(self):
        return self.discounted_price is not None and self.discounted_price < self.price


class UserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    unlocked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.book}"
    

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name