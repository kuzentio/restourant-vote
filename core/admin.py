from django.contrib import admin

from core.models import Restaurant, UserRating, RestaurantRating


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'food_type', 'city', 'address')


@admin.register(UserRating)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'rating', 'review')


@admin.register(RestaurantRating)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'get_avg_rating')

    def get_avg_rating(self, obj):
        return obj.total_rating / obj.total_voters
    get_avg_rating.short_description = 'Average rating'
