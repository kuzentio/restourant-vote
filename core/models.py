from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver


class Restaurant(models.Model):
    FINE_DINING = 'Fine Dining'
    CASUAL = 'Casual'
    FAST_FOOD = 'Fast Food'
    BUFFET = 'Buffet'
    PUB = 'Pub'
    FOOD_TYPE_CHOICES = (
        (FINE_DINING, FINE_DINING),
        (CASUAL, CASUAL),
        (FAST_FOOD, FAST_FOOD),
        (BUFFET, BUFFET),
        (PUB, PUB),
    )
    name = models.CharField(max_length=255)
    food_type = models.CharField(choices=FOOD_TYPE_CHOICES, max_length=100, blank=True)
    city = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name


class RestaurantRating(models.Model):
    ZERO_VOTE = 0.0
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    total_rating = models.FloatField(default=ZERO_VOTE)
    total_voters = models.FloatField(default=ZERO_VOTE)


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
def update_rating(sender, instance, created, **kwargs):
    rating, _ = RestaurantRating.objects.get_or_create(
        restaurant=instance.restaurant,
    )
    if created:
        rating.total_rating += instance.rating
        rating.total_voters += 1
    else:
        qs = UserRating.objects.filter(
            restaurant=instance.restaurant
        )
        rating.total_rating = qs.aggregate(Sum('rating'))['rating__sum']
        rating.total_voters = qs.count()

    rating.save()
