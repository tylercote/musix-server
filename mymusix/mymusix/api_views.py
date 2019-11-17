from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F, OuterRef
from django.http import JsonResponse
from . import models
from . import serializers
from .serializers import NewConcertSerializer
from .models import Artist
from .models import Venue
from .models import Concert
from .models import Review
from django.db.models.base import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import connection


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


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

    @action(detail=True)
    def get_artists(self, request, pk):
        festival = self.get_object()
        data = list(festival.artists.values())
        return JsonResponse(data, safe=False)

class ConcertViewset(viewsets.ModelViewSet):
    queryset = models.Concert.objects.all()
    serializer_class = serializers.ConcertSerializer

    @action(detail=False)
    def get_concerts(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT c.id, c.artist_id, c.venue_id, c.festival_id, a.name as artistName, c.date, v.name as venueName, v.location as venueLocation, f.name as festivalName, r.id as review_id, r.stars, r.comments "
                           "FROM concerts AS c "
                           "JOIN artists AS a ON c.artist_id = a.id "
                           "JOIN venues AS v ON c.venue_id = v.id  "
                           "LEFT JOIN festivals AS f ON c.festival_id = f.id "
                           "LEFT JOIN reviews as r ON c.id = r.concert_id;")
            # rows = cursor.fetchall()
            rowDict = dictfetchall(cursor)
            return JsonResponse(rowDict, safe=False)

    @action(detail=False, methods=["post"])
    def add_concert(self, request):
        serializer = NewConcertSerializer(data=request.data)
        serializer.is_valid()
        concert = Concert()
        concert.date = serializer.data["date"]
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
            venue = Venue.objects.filter(name=serializer.data["venueName"], location=serializer.data["venueLocation"])[:1].get()
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