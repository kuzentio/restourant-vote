from rest_framework import serializers

from core.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ('name',
                  'food_type',
                  'city', 'address', 'average_rating')

    def get_average_rating(self, obj):
        if not hasattr('obj', 'restaurantrating'):
            return round(0.0, 2)
        return round(obj.restaurantrating.total_rating / obj.restaurantrating.total_voters, 2)
