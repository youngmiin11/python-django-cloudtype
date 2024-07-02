from django.urls import path
from .views import post_user_info, check_user_id, crawl_user_info, login_user

urlpatterns = [
    path('user/info/', post_user_info, name='post_user_info'),
    path('user/info/<str:user_id>/', check_user_id, name='check_user_id'),
    path('user/crawl/', crawl_user_info, name='crawl_user_info'),
    path('login/', login_user, name='login_user'),
]
