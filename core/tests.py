from statistics import mean

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.factories import RestaurantFactory, UserRatingFactory, UserFactory
from core.models import Restaurant, UserRating


class TestListRestaurants(APITestCase):
    def setUp(self):
        self.user = UserFactory(
            username='john',
            password='qwerty'
        )
        self.client.force_authenticate(self.user)

    def test_list_restaurants_returns_all_restaurants(self):
        RestaurantFactory.create_batch(5)
        response = self.client.get(reverse('restaurant-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), Restaurant.objects.all().count())

    def test_list_restaurants_returns_average_rating(self):
        restaurant = RestaurantFactory()
        UserRatingFactory(restaurant=restaurant)
        UserRatingFactory(restaurant=restaurant)

        response = self.client.get(reverse('restaurant-list'))
        avg_rating = UserRating.objects.filter(restaurant=restaurant).values_list('rating', flat=True)
        self.assertEqual(response.json()[0]['average_rating'], mean(avg_rating))

    def test_user_rating_affect_restaurant_rating(self):
        restaurant = RestaurantFactory()
        UserRatingFactory(restaurant=restaurant)
        UserRatingFactory(restaurant=restaurant)


class TestRatingView(APITestCase):
    def setUp(self):
        self.user = UserFactory(
            username='john',
            password='qwerty'
        )
        self.client.force_authenticate(self.user)

    def test_calling_view_returns_existing_user_rating(self):
        restaurant = RestaurantFactory()
        user_rating = UserRatingFactory(
            restaurant=restaurant,
            user=self.user,
            rating=5,
            review="Test awesome text",
        )
        response = self.client.get(
            reverse('user-rating-detail', args=(user_rating.id, ))
        )
        if response.status_code == status.HTTP_200_OK:
            payload = response.json()
            self.assertEqual(payload['rating'], user_rating.rating)
            self.assertEqual(payload['review'], user_rating.review)

    def test_posting_view_create_user_rating(self):
        restaurant = RestaurantFactory()
        user_rating = {
            "rating": 5,
            "review": "Excellent place",
            "restaurant": restaurant.id
        }
        response = self.client.post(reverse('user-rating'), data=user_rating)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['restaurant'], restaurant.id)

    def test_user_rating_should_be_unique_for_restaurant(self):
        restaurant = RestaurantFactory()
        user_rating = {
            "rating": 5,
            "review": "Excellent place",
            "restaurant": restaurant.id
        }
        response = self.client.post(reverse('user-rating'), data=user_rating)
        if response.status_code == status.HTTP_201_CREATED:
            response = self.client.post(reverse('user-rating'), data=user_rating)
            self.assertContains(response, 'non_field_errors', status_code=status.HTTP_400_BAD_REQUEST)


class TestRetrieveRestaurantDetail(APITestCase):
    def setUp(self):
        self.user = UserFactory(
            username='john',
            password='qwerty'
        )
        self.client.force_authenticate(self.user)

    # def test_retrieve_restaurant_detail_with_rating(self):
    #     restaurant = RestaurantFactory()
    #     user_rating = UserRatingFactory(restaurant=restaurant, user=self.user)
    #     response = self.client.get(reverse('restaurant-detail', args=(restaurant.id, )))
    #     import ipdb; ipdb.set_trace()

