from django.contrib import admin
from django.urls import path
from api.urls import restaurant_list, restaurant_detail


urlpatterns = [
    path('admin/', admin.site.urls),

    path('restaurant/all', restaurant_list, name='restaurant-list'),
    path('restaurant/<int:pk>', restaurant_detail, name='restaurant-detail'),
]
