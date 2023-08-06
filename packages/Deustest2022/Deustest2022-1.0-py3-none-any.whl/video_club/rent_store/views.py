from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import CustomUser, Category, Movie, Rental
from .serializers import ProfileSerializer, ProfileUpdateSerializer, MovieCategorySerializer, MovieSerializer, \
    RentalCreateSerializer, RentalUpdateSerializer, RentalSerializer, MovieCreateSerializer
from .utils.queryset_operations import filter_movies, order_movies, filter_rentals


def index(request):
    return render(request, "index.html")


class Pagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        return {
            "retrieve": ProfileSerializer,
            "partial_update": ProfileUpdateSerializer
        }.get(self.action)

    @swagger_auto_schema(operation_description="Get the user's profile.")
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="Update a user profile. Only deposit is supported.")
    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class MovieCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = MovieCategorySerializer
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(operation_description="Get the list of movie categories.")
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)


class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    pagination_class = Pagination
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        return {
            "create": MovieCreateSerializer
        }.get(self.action, MovieSerializer)

    def get_permissions(self):
        if self.request.method == 'POST':
            # allow only admin user to create new movies
            permission_classes = (IsAuthenticated, IsAdminUser, )
            return [permission() for permission in permission_classes]
        else:
            return [permission() for permission in self.permission_classes]

    def get_object(self, pk):
        try:
            obj = Movie.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except ObjectDoesNotExist:
            raise NotFound

    @swagger_auto_schema(operation_description="Get a list of all movies."
                                               "Filter params: [category, from-rating, to-rating, from-year, to-year], "
                                               "Order params: orderBy")
    def list(self, request, *args, **kwargs):
        queryset = filter_movies(request.query_params, self.queryset)
        queryset = order_movies(request.query_params, queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(data=page, many=True)
            serializer.is_valid()
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(data=queryset, many=True)
            serializer.is_valid()
            return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="Get a specific movie.")
    def retrieve(self, request, *args, **kwargs):
        try:
            movie = self.get_object(kwargs['movie_uuid'])
            serializer = self.get_serializer(movie)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Create a movie.")
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class MovieRentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalCreateSerializer
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        return {
            "list": RentalSerializer,
            "retrieve": RentalSerializer,
            "create": RentalCreateSerializer,
            "partial_update": RentalUpdateSerializer
        }.get(self.action)

    @swagger_auto_schema(operation_description="Get a list of all rentals associated to the user."
                                               "Can filter with 'only-active'")
    def list(self, request, *args, **kwargs):
        queryset = Rental.objects.filter(user=request.user)
        queryset = filter_rentals(request.query_params, queryset)
        serializer = self.get_serializer(data=queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="Get a specific rental.")
    def retrieve(self, request, *args, **kwargs):
        try:
            rental = Rental.objects.get(uuid=kwargs['rental_uuid'])
            serializer = self.get_serializer(rental)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Rent a movie.")
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_description="Return a movie and subtract charge from users wallet.")
    def partial_update(self, request, *args, **kwargs):
        rental = Rental.objects.get(uuid=kwargs["rental_uuid"])
        request.data["rental"] = rental

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Movie returned successfully.", status=status.HTTP_200_OK)
