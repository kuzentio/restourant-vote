from django.contrib import admin
from django.urls import path
from api.urls import restaurant_list, restaurant_detail, user_rating_detail
from core.views import index

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/restaurant/all/', restaurant_list, name='restaurant-list'),
    path('api/restaurant/<int:pk>/', restaurant_detail, name='restaurant-detail'),
    path('api/user-rating/', user_rating_detail, name='user-rating'),
    path('api/user-rating/<int:restaurant>/', user_rating_detail, name='user-rating-detail'),
    # path('api/user-rating/update/<int:pk>/', user_rating_detail, name='user-rating-detail'),

    path("", index, name="index"),
]
