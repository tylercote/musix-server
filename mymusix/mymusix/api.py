from rest_framework import routers
from mymusix import api_views


router = routers.DefaultRouter()
router.register(r'genres', api_views.GenreViewset)
router.register(r'artists', api_views.ArtistViewset)
router.register(r'venues', api_views.VenueViewset)
router.register(r'festivals', api_views.FestivalViewset)
router.register(r'concerts', api_views.ConcertViewset)
router.register(r'reviews', api_views.ReviewViewset)
