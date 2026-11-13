from django.urls import path
from users.apps import UsersConfig

from users.views import (CreateUserAPIView,
                         ListUserAPIView,
                         SingleUserAPIView,
                         UpdateUserAPIView,
                         DeleteUserAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path('user/create', CreateUserAPIView.as_view(), name='create_user'),
    path('users/list/', ListUserAPIView.as_view(), name='list_users'),
    path('user/<int:pk>/', SingleUserAPIView.as_view(), name='single_user'),
    path('user/update/<int:pk>/', UpdateUserAPIView.as_view(), name='update_user'),
    path('user/delete/<int:pk>/', DeleteUserAPIView.as_view(), name='delete_user'),
]
