from rest_framework import serializers
from .models import Category, Movie, MovieCategoryAssociation, Rental, CustomUser
from rest_framework import exceptions
from django.db import transaction
import datetime


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'wallet', )


class ProfileUpdateSerializer(serializers.ModelSerializer):
    deposit = serializers.FloatField(default=0.0)

    def to_representation(self, instance):
        user = self.context["request"].user
        representation = super(ProfileUpdateSerializer, self).to_representation(instance)
        representation["email"] = user.email
        representation["first_name"] = user.first_name
        representation["last_name"] = user.last_name
        representation["wallet"] = user.wallet
        return representation

    def save(self, **kwargs):
        req_data = self.context["request"].data
        user = self.context["request"].user
        user.wallet += req_data['deposit']
        user.save()

    def validate(self, attrs):
        # accept only positive deposits
        if "deposit" not in self.context["request"].data or attrs["deposit"] < 0:
            raise exceptions.ValidationError
        return attrs

    class Meta:
        model = CustomUser
        fields = ('deposit', )


class MovieCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name',)


class MovieSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super(MovieSerializer, self).to_representation(instance)
        associations = MovieCategoryAssociation.objects.filter(movie=instance)
        representation['categories'] = [a.category.name for a in associations]
        return representation

    class Meta:
        model = Movie
        exclude = ()


class MovieCreateSerializer(serializers.ModelSerializer):
    categories = serializers.CharField(max_length=100, allow_blank=True, allow_null=True)

    def save(self, **kwargs):
        req_data = self.context["request"].data
        movie_dict = {
            "name": req_data["name"],
            "pub_date": req_data["pub_date"],
            "duration": req_data["duration"],
            "rating": req_data["rating"],
            "description": req_data["description"],
        }
        movie = Movie(**movie_dict)
        with transaction.atomic():
            movie.save()
            cats = [s.strip() for s in req_data["categories"].split(",")]
            for cat in cats:
                category = Category.objects.get(name=cat)
                assoc = MovieCategoryAssociation(movie=movie, category=category)
                assoc.save()

    def validate(self, attrs):
        # check if categories are valid
        cats = [s.strip() for s in attrs["categories"].split(",")]
        try:
            [Category.objects.get(name=cat) for cat in cats]
        except:
            raise exceptions.ValidationError
        return attrs

    class Meta:
        model = Movie
        fields = ('name', 'pub_date', 'duration', 'rating', 'description', 'categories')


class RentalCreateSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        user = self.context["request"].user
        movie = Movie.objects.get(uuid=self.context["request"].data["movie"])
        data = {"user": user, "movie": movie}
        rental = Rental(**data)
        rental.save()

    def to_representation(self, instance):
        representation = super(RentalCreateSerializer, self).to_representation(instance)
        representation["user"] = self.context["request"].user.email
        representation["movie"] = instance["movie"].name
        representation["rental_date"] = str(
            Rental.objects.get(user=self.context["request"].user, movie=instance["movie"], return_date=None).rental_date
        )
        return representation

    def validate(self, attrs):
        # if association exists and is not returned throw exception
        user = self.context["request"].user
        movie = attrs["movie"]
        rentals = Rental.objects.filter(user=user, movie=movie)
        if len(rentals) > 0 and any([r.return_date is None for r in rentals]):
            raise exceptions.ValidationError
        return attrs

    class Meta:
        model = Rental
        fields = ('movie', )


class RentalUpdateSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        # check if there are enough money in the wallet
        rental = self.context["request"].data["rental"]
        user = self.context["request"].user
        if rental.is_paid:
            raise exceptions.ValidationError("Movie already returned.")
        if rental.calculate_charge() > user.wallet:
            raise exceptions.ValidationError("Not enough money in your wallet.")
        return attrs

    def save(self, **kwargs):
        rental = self.context["request"].data["rental"]
        rental.return_date = datetime.date.today()
        rental.is_paid = True
        user = self.context["request"].user
        user.wallet -= rental.calculate_charge()
        with transaction.atomic():
            rental.save()
            user.save()

    class Meta:
        model = Rental
        fields = ()


class RentalSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super(RentalSerializer, self).to_representation(instance)
        representation["user"] = instance.user.email
        representation["movie"] = instance.movie.name
        representation["charge"] = instance.calculate_charge()
        return representation

    class Meta:
        model = Rental
        exclude = ()