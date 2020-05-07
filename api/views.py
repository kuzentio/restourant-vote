from django.db.models import F
from rest_framework import viewsets
from core.models import Restaurant
from core.serializers import RestaurantSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    
    def filter_queryset(self, queryset):
        qs = super(RestaurantViewSet, self).filter_queryset(queryset)
        if self.request.query_params.get('orderBy') == 'recommended':
            qs = qs.annotate(
                avg_rating=F('restaurantrating__total_rating') / F('restaurantrating__total_voters')
            ).order_by('-avg_rating')
        elif self.request.query_params.get('orderBy') == 'most_reviewed':
            qs = qs.order_by('-restaurantrating__total_voters')
        elif self.request.query_params.get('orderBy') == 'most_rated':
            qs = qs.order_by('-restaurantrating__total_rating')

        return qs
