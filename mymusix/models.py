from django.db import models
from django.conf import settings

class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "genres"


class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre)

    class Meta:
        db_table = "artists"


class Venue(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    class Meta:
        db_table = "venues"


class Festival(models.Model):
    id = models.AutoField(primary_key=True)
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    startdate = models.DateField()
    enddate = models.DateField()
    artists = models.ManyToManyField(Artist)

    class Meta:
        db_table = "festivals"


class Concert(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 null=True, blank=True, on_delete=models.SET_NULL)
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT)
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT)
    festival = models.ForeignKey(Festival, blank=True, null=True, on_delete=models.SET_NULL)
    date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "concerts"


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=True, blank=True, on_delete=models.SET_NULL)
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)
    stars = models.DecimalField(decimal_places=2, max_digits=3, null=True, blank=True)
    comments = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        db_table = "reviews"
