from django.contrib import admin

from core.models import Restaurant, UserVote


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'food_type', 'city', 'address')


@admin.register(UserVote)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'rate', 'review')
