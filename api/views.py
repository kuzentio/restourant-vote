from django.db.models import F, When, FloatField, Case
from rest_framework import viewsets
from core.models import Restaurant
from core.serializers import RestaurantSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    
    def filter_queryset(self, queryset):
        qs = super(RestaurantViewSet, self).filter_queryset(queryset)
        if self.request.query_params.get('order_by') == 'recommended':
            qs = qs.annotate(
                avg_rating=Case(
                    When(
                        restaurantrating__total_voters__gt=0,
                        then=F('restaurantrating__total_rating') / F('restaurantrating__total_voters'),
                    ),
                    default=0.0,
                    output_fields=FloatField(),
                )
            ).order_by(
                '-avg_rating'
            )
        if self.request.query_params.get('order_by') == 'most_reviewed':
            qs.order_by('-restaurantrating__total_voters')
        elif self.request.query_params.get('order_by') == 'most_rated':
            qs.order_by('-restaurantrating__total_rating')
        return qs
