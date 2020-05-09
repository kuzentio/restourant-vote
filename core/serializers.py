from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from core.models import Restaurant, UserRating


class RestaurantSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Restaurant
        fields = (
            'id', 'name', 'food_type', 'city', 'address', 'average_rating'
        )

    @staticmethod
    def get_average_rating(obj):
        if not hasattr(obj, 'restaurantrating') or not obj.restaurantrating.total_voters:
            return round(0.0, 2)
        return round(obj.restaurantrating.total_rating / obj.restaurantrating.total_voters, 2)


class UserRatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserRating
        fields = (
            'restaurant', 'rating', 'review', 'user'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=UserRating.objects.all(),
                fields=['user', 'restaurant']
            )
        ]
