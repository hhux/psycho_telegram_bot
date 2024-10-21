from django.contrib import admin
from django.urls import path
from app.views import UserListView, UserCreateView, deactivate_users

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('deactivate_users/', deactivate_users, name='deactivate-users'),
]
