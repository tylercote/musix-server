from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.renderers import JSONRenderer
from . import models
from . import serializers
from .serializers import NewConcertSerializer
from .models import Artist
from .models import Venue
from .models import Concert
from .models import Review
from django.db.models.base import ObjectDoesNotExist


class GenreViewset(viewsets.ModelViewSet):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class ArtistViewset(viewsets.ModelViewSet):
    queryset = models.Artist.objects.all()
    serializer_class = serializers.ArtistSerializer


class VenueViewset(viewsets.ModelViewSet):
    queryset = models.Venue.objects.all()
    serializer_class = serializers.VenueSerializer


class FestivalViewset(viewsets.ModelViewSet):
    queryset = models.Festival.objects.all()
    serializer_class = serializers.FestivalSerializer


class ConcertViewset(viewsets.ModelViewSet):
    queryset = models.Concert.objects.all()
    serializer_class = serializers.ConcertSerializer

    @action(detail=False, methods=["post"])
    def add_concert(self, request):
        serializer = NewConcertSerializer(data=request.data)
        serializer.is_valid()
        concert = Concert()
        concert.date = serializer.data["date"]
        print(serializer.data)
        try:
            artist = Artist.objects.get(name=serializer.data["artist"])
            concert.artist_id = artist.pk
        except ObjectDoesNotExist:
            print("Artist not in DB, making new artist...")
            newArtist = Artist()
            newArtist.name = serializer.data["artist"]
            newArtist.save()
            concert.artist_id = newArtist.pk

        try:
            venue = Venue.objects.get(name=serializer.data["venueName"], location=serializer.data["venueLocation"])
            concert.venue_id = venue.pk
        except ObjectDoesNotExist:
            print("Venue not in DB, making new venue...")
            newVenue = Venue()
            newVenue.name = serializer.data["venueName"]
            newVenue.location = serializer.data["venueLocation"]
            newVenue.save()
            concert.venue_id = newVenue.pk

        concert.save()

        newReview = Review()
        newReview.concert_id = concert.pk
        newReview.stars = serializer.data["rating"]
        newReview.comments = serializer.data["comments"]
        newReview.save()

        return Response(serializer.data)


class ReviewViewset(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer