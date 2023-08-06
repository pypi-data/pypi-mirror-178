from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', views.index, name='index'),
    url('^', include(router.urls)),
    url('^profile/$', views.ProfileViewSet.as_view({"get": "retrieve", "patch": "partial_update"}), name='profile'),
    url('^movies/$', views.MovieViewSet.as_view({"get": "list", "post": "create"}), name='movies'),
    url('^movies/(?P<movie_uuid>.+)$', views.MovieViewSet.as_view({"get": "retrieve"}), name='movie'),
    url('^categories', views.MovieCategoryViewSet.as_view({"get": "list"}), name='categories'),
    url('^rentals/$', views.MovieRentalViewSet.as_view(
        {"get": "list", "post": "create"}
    ), name='rentals'),
    url('^rentals/(?P<rental_uuid>.+)$', views.MovieRentalViewSet.as_view(
        {"get": "retrieve", "patch": "partial_update"}
    ), name='rental')
]