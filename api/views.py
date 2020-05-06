from rest_framework import viewsets
from core.models import Restaurant
from core.serializers import RestaurantSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    # authentication_classes = []
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
