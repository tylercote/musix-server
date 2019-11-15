from rest_framework import serializers
# from rest_framework_json_api import serializers

from . import models


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