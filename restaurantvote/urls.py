from django.contrib import admin
from django.urls import path
from api.urls import restaurant_list, restaurant_detail
from core.views import index

urlpatterns = [
    path('admin/', admin.site.urls),

    path('restaurant/all/', restaurant_list, name='restaurant-list'),
    path('restaurant/<int:pk>/', restaurant_detail, name='restaurant-detail'),

    path("", index, name="index"),
]
