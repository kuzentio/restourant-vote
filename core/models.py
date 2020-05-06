from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Restaurant(models.Model):
    FINE_DINING = 1
    CASUAL = 2
    FAST_FOOD = 3
    BUFFET = 4
    PUB = 5
    FOOD_TYPE_CHOICES = (
        (FINE_DINING, 'Fine Dining'),
        (CASUAL, 'Casual'),
        (FAST_FOOD, 'Fast Food'),
        (BUFFET, 'Buffet'),
        (PUB, 'Pub'),
    )
    name = models.CharField(max_length=255)
    food_type = models.IntegerField(choices=FOOD_TYPE_CHOICES)
    city = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name


class RestaurantRating(models.Model):
    ZERO_VOTE = 0
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    total_rating = models.PositiveIntegerField(default=ZERO_VOTE)
    total_voters = models.PositiveIntegerField(default=ZERO_VOTE)


class UserRating(models.Model):
    POOR_RATING = 1
    AVERAGE_RATING = 2
    GOOD_RATING = 3
    VERY_GOOD_RATING = 4
    EXCELLENT_RATING = 5
    RATING_CHOICES = (
        (POOR_RATING, 'Poor'),
        (AVERAGE_RATING, 'Average'),
        (GOOD_RATING, 'Good'),
        (VERY_GOOD_RATING, 'Very Good'),
        (EXCELLENT_RATING, 'Excellent')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES, default=GOOD_RATING)
    review = models.TextField()

    class Meta:
        unique_together = ('user', 'restaurant')

    def __str__(self):
        return "{0}:{1}".format(self.restaurant, self.rating)


@receiver(post_save, sender=UserRating, dispatch_uid="update_restaurant_rating")
def update_rating(sender, instance, **kwargs):
    try:
        rating = instance.restaurant.restaurantrating
    except RestaurantRating.DoesNotExist:
        rating = RestaurantRating.objects.create(
            restaurant=instance.restaurant,
        )
    rating.total_rating += instance.rating
    rating.total_voters += 1
    rating.save()
