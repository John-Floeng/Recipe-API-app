"""
URL mappings for the user API.
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from user import views

app_name = 'user'

urlpatterns = [
    path('api/create/', views.CreateUserView.as_view(), name='create'),
    path('api/token/', views.CreateTokenView.as_view(), name='token'),
    path('api/me/', views.ManageUserView.as_view(), name='me'),
    path('create/', views.UserCreateView.as_view(), name='create_user'),
    path('create/confirmed/', views.UserCreateView.user_created, name='user_created'),
    path('login/', views.UserLoginView.as_view(), name='login' ),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout')
]