from api.views import RestaurantViewSet, UserRatingViewSet

restaurant_list = RestaurantViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
restaurant_detail = RestaurantViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})
user_rating_detail = UserRatingViewSet.as_view({
    'post': 'update',
    'get': 'retrieve',
})
