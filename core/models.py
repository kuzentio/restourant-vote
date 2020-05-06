from django.contrib.auth.models import User
from django.db import models


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


class UserVote(models.Model):
    POOR_RATE = 1
    AVERAGE_RATE = 2
    GOOD_RATE = 3
    VERY_GOOD_RATE = 4
    EXCELLENT_RATE = 5
    RATE_CHOICES = (
        (POOR_RATE, 'Poor'),
        (AVERAGE_RATE, 'Average'),
        (GOOD_RATE, 'Good'),
        (VERY_GOOD_RATE, 'Very Good'),
        (EXCELLENT_RATE, 'Excellent')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rate = models.IntegerField(choices=RATE_CHOICES, default=GOOD_RATE)
    review = models.TextField()

    class Meta:
        unique_together = ('user', 'restaurant')

    def __str__(self):
        return "{0}:{1}".format(self.restaurant, self.rate)
