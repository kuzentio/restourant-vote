from django.core.management import BaseCommand

from core.factories import UserFactory, RestaurantFactory, UserRatingFactory


class Command(BaseCommand):
    help = 'Load fake data to DB'

    def handle(self, *args, **options):
        for _ in range(4):
            restaurant = RestaurantFactory()
            for _ in range(5):
                UserRatingFactory(restaurant=restaurant)
