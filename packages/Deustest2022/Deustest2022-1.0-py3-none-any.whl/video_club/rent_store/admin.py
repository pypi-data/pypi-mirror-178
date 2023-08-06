from django.contrib import admin

# Register your models here.
from .models import Category, CustomUser, Movie, MovieCategoryAssociation, Rental

admin.site.register(Category)
admin.site.register(CustomUser)
admin.site.register(Movie)
admin.site.register(MovieCategoryAssociation)
admin.site.register(Rental)