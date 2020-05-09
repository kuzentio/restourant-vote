from django.db.models import F, When, FloatField, Case
from django.http import Http404
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Restaurant, UserRating
from core.serializers import RestaurantSerializer, UserRatingSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, ]

    def filter_queryset(self, queryset):
        qs = super(RestaurantViewSet, self).filter_queryset(queryset)
        order_by = self.request.query_params.get('order_by')
        if order_by == 'recommended':
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
        elif order_by == 'default':
            qs = qs.order_by('-pk')
        return qs


class UserRatingViewSet(viewsets.ModelViewSet):
    serializer_class = UserRatingSerializer
    queryset = UserRating.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'restaurant'

    def filter_queryset(self, queryset):
        qs = super(UserRatingViewSet, self).filter_queryset(queryset)
        return qs.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
        except Http404:
            return super().create(request, *args, **kwargs)
        return response
