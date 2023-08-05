from plex import Plex
from plex.objects.core.base import Property, DescriptorMixin


class RateMixin(DescriptorMixin):
    user_rating = Property('userRating', float)

    def rate(self, value):
        return Plex['library'].rate(self.rating_key, value)
