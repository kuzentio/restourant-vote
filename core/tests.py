from django.db.models import Avg, Subquery, IntegerField, Count, Sum, OuterRef, Prefetch
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from core.factories import RestaurantFactory, UserRatingFactory
from core.models import Restaurant, UserRating


class Test(TestCase):
    def setUp(self):
        RestaurantFactory.create_batch(5)

    def test_list_restaurants_returns_all_restaurants(self):
        response = self.client.get(reverse('restaurant-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), Restaurant.objects.all().count())

    def test_list_restaurants_returns_average_rating(self):
        restaurant = Restaurant.objects.first()
        user_rating = UserRatingFactory.create(
            restaurant=restaurant,
            rating=UserRating.EXCELLENT_RATING
        )
        UserRatingFactory.create(
            restaurant=restaurant,
            rating=UserRating.AVERAGE_RATING
        )

        qs = Restaurant.objects.all()
        import ipdb; ipdb.set_trace()
        # qs = Restaurant.objects.annotate(
        #     total_voters=Subquery(
        #         UserRating.objects.filter(
        #             restaurant__pk=OuterRef('pk')
        #         ).values(
        #             'restaurant'
        #         ).annotate(
        #             count_voters=Count('pk')
        #         ).values(
        #             'count_voters'
        #         )
        #     ),
        #     total_rating=Subquery(
        #         UserRating.objects.filter(
        #             restaurant__pk=OuterRef('pk')
        #         ).values(
        #             'restaurant'
        #         ).annotate(
        #             sum_rating=Sum('rating')
        #         ).values(
        #             'sum_rating'
        #         )
        #     )
        # )


        # response = self.client.get(reverse('restaurant-list'))
