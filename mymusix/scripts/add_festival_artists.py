from mymusix.models import Artist
from mymusix.models import Festival
from mymusix.models import Venue
from django.db.models.base import ObjectDoesNotExist
import os


# Script to add a new festival with its details and listed artists (from text file)

# input file:
# first line - venueName, venueLocation, festivalName, festivalStartDate, festivalEndDate
# remaining lines - artistName
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def run():
    with open(os.path.join(__location__, 'osheaga2019'), 'r') as f:

        i = 0
        newFestival = Festival()

        for line in f:
            line = line.strip()
            # Parse header line
            if i == 0:
                venueName, venueLocation, festivalName, festivalStartDate, festivalEndDate = line.split('|')
                newFestival.name = festivalName
                newFestival.startDate = festivalStartDate
                newFestival.endDate = festivalEndDate
                try:
                    venue = Venue.objects.get(name=venueName, location=venueLocation)
                    newFestival.venue_id = venue.pk
                except ObjectDoesNotExist:
                    print("Venue not in DB, making new venue...")
                    newVenue = Venue()
                    newVenue.name = venueName
                    newVenue.location = venueLocation
                    newVenue.save()
                    newFestival.venue_id = newVenue.pk
                newFestival.save()

            # Parse artist lines
            else:
                # Make artist if not exist
                try:
                    artist = Artist.objects.get(name=line)
                    newFestival.artists.add(artist)
                except ObjectDoesNotExist:
                    print("Artist not in DB, making new artist...")
                    newArtist = Artist()
                    newArtist.name = line
                    newArtist.save()
                    newFestival.artists.add(newArtist)
            i += 1