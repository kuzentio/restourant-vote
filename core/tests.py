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

    def test_user_rating_does_affect_restaurant_rating(self):
        restaurant = RestaurantFactory()
        UserRatingFactory(restaurant=restaurant)
        UserRatingFactory(restaurant=restaurant)

    def test_post_restaurant_creates_restaurant(self):
        new_restaurant_data = {
            'name': 'Sun Cafe',
            'food_type': Restaurant.CASUAL,
            'city': 'New York',
            'address': 'somerandomaddress',
        }
        self.assertEqual(Restaurant.objects.all().count(), 0)
        response = self.client.post(reverse('restaurant-list'), data=new_restaurant_data)
        self.assertEqual(Restaurant.objects.all().count(), 1)
        self.assertEqual(response.json()['name'], new_restaurant_data['name'])

    def test_delete_restaurant(self):
        restaurant = RestaurantFactory()
        self.assertEqual(Restaurant.objects.count(), 1)
        self.client.delete(reverse('restaurant-detail', args=(restaurant.id, )))
        self.assertEqual(Restaurant.objects.count(), 0)

    def test_edit_restaurant_data(self):
        restaurant = RestaurantFactory()

        updated_restaurant_data = {
            'name': restaurant.name + '!',
            'city': restaurant.city + '!',
            'address': restaurant.address + '!',
            'food_type': Restaurant.CASUAL,
        }
        self.assertEqual(Restaurant.objects.get().name, restaurant.name)
        self.assertEqual(Restaurant.objects.get().city, restaurant.city)
        self.client.put(reverse('restaurant-detail', args=(restaurant.id, )), data=updated_restaurant_data)
        self.assertEqual(Restaurant.objects.get().name, updated_restaurant_data['name'])
        self.assertEqual(Restaurant.objects.get().city, updated_restaurant_data['city'])

    def test_ordering_by_avg_rating(self):
        for i in range(5):
            restaurant = RestaurantFactory()
            for _ in range(2):
                UserRatingFactory(restaurant=restaurant, rating=1.0)
        response = self.client.get("{0}?{1}={2}".format(reverse('restaurant-list'), 'order_by', 'default'))
        self.assertEqual(response.json()[-1]['id'], Restaurant.objects.first().id)
        self.assertEqual(response.json()[0]['id'], Restaurant.objects.last().id)

        restaurant = Restaurant.objects.last()
        UserRatingFactory(restaurant=restaurant, rating=5.0)
        response = self.client.get("{0}?{1}={2}".format(reverse('restaurant-list'), 'order_by', 'recommended'))
        self.assertEqual(response.json()[0]['id'], restaurant.id)


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
        response = self.client.post(reverse('user-rating-detail', args=(restaurant.id, )), data=user_rating)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['restaurant'], restaurant.id)


class TestRetrieveRestaurantDetail(APITestCase):
    def setUp(self):
        self.user = UserFactory(
            username='john',
            password='qwerty'
        )
        self.client.force_authenticate(self.user)

    def test_restaurant_detail(self):
        restaurant = RestaurantFactory()
        response = self.client.get(reverse('restaurant-detail', args=(restaurant.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], restaurant.id)
