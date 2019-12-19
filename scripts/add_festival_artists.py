from mymusix.models import Artist
from mymusix.models import Festival
from mymusix.models import Venue
from django.db.models.base import ObjectDoesNotExist
import os
import sys


# Script to add a new festival with its details and listed artists (from text file)

# input file:
# first line - venueName, venueLocation, festivalName, festivalStartDate, festivalEndDate
# remaining lines - artistName
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def run():

    print(sys.argv)

    festival = sys.argv[1]

    with open(os.path.join(__location__, festival), 'r') as f:
        i = 0
        newFestival = Festival()

        for line in f:
            line = line.strip()
            # Parse header line
            if i == 0:
                venuename, venuelocation, festivalname, festivalstartdate, festivalenddate = line.split('|')
                newFestival.name = festivalname
                newFestival.startdate = festivalstartdate
                newFestival.enddate = festivalenddate
                try:
                    venue = Venue.objects.get(name=venuename, location=venuelocation)
                    newFestival.venue_id = venue.pk
                except ObjectDoesNotExist:
                    print("Venue not in DB, making new venue...")
                    newVenue = Venue()
                    newVenue.name = venuename
                    newVenue.location = venuelocation
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