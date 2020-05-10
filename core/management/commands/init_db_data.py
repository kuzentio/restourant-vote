from django.core.management import BaseCommand

from core.factories import RestaurantFactory, UserRatingFactory, FAKE_RESTAURANT_NAMES


class Command(BaseCommand):
    help = 'Load fake data to DB'

    def handle(self, *args, **options):
        for restaurant_name in FAKE_RESTAURANT_NAMES:
            restaurant = RestaurantFactory(name=restaurant_name)
            for _ in range(5):
                UserRatingFactory(restaurant=restaurant)
