from rest_framework import serializers

from core.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Restaurant
        fields = (
            'id', 'name', 'food_type', 'city', 'address', 'average_rating'
        )

    @staticmethod
    def get_average_rating(obj):
        if not hasattr(obj, 'restaurantrating') or not obj.restaurantrating.total_voters > 0:
            return round(0.0, 2)
        return round(obj.restaurantrating.total_rating / obj.restaurantrating.total_voters, 2)
