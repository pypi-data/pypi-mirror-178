from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import datetime


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    wallet = models.FloatField(default=0)
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.email


class Movie(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    pub_date = models.PositiveSmallIntegerField(blank=True, null=True)
    duration = models.PositiveSmallIntegerField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class MovieCategoryAssociation(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Rental(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT)
    rental_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    def calculate_charge(self):
        end_date = self.return_date if self.return_date else datetime.date.today()
        delta = end_date - self.rental_date
        no_days = delta.days + 1
        if no_days <= 3:
            return no_days
        else:
            return 3 + (no_days - 3) * 0.5

    def __str__(self):
        return str(self.user) + " -> " + str(self.movie)
