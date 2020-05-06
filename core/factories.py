import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from factory.fuzzy import FuzzyChoice

from core.models import Restaurant, UserVote

FAKE_RESTAURANT_NAMES = [
    'Blue & Seafood Bar', 'The Cuban', 'Amanda\'s', 'Monroe\'s'
]


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    first_name = "John"
    last_name = "Doe"
    username = factory.Sequence(lambda n: 'j_doe%s' % n)
    password = make_password('password')


class RestaurantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Restaurant

    name = FuzzyChoice(FAKE_RESTAURANT_NAMES)
    food_type = FuzzyChoice([food_type[0] for food_type in Restaurant.FOOD_TYPE_CHOICES])
    city = 'New York'
    address = 'Test address'


class UserVoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserVote
    user = factory.SubFactory(UserFactory)
    restaurant = factory.SubFactory(RestaurantFactory)
    rate = FuzzyChoice([rate[0] for rate in UserVote.RATE_CHOICES])
    review = 'Some random text'
