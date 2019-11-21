from rest_framework import serializers
from . import models
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'password')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ('id', 'name')


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Artist
        fields = ('id', 'name')


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Venue
        fields = ('id', 'name', 'location')


class FestivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Festival
        fields = ('id', 'venue', 'name', 'startDate', 'endDate')


class ConcertSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Concert
        fields = ('id', 'artist', 'venue', 'festival', 'date')


class NewConcertSerializer(serializers.Serializer):
    artist = serializers.CharField()
    rating = serializers.DecimalField(decimal_places=2, max_digits=3)
    comments = serializers.CharField()
    date = serializers.DateField()
    venueName = serializers.CharField()
    venueLocation = serializers.CharField()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ('id', 'concert', 'stars', 'comments')