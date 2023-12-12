"""
Views for the user API.
"""
from django import forms
from django.shortcuts import render, redirect
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from core.models import User
from .forms import UserCreationForm

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer
)


####################################################################
##################  API Views ############


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
    

###################################################################
#############  Front end page Views ###########


class UserCreateView(CreateView):
    """Create a new user."""
    model = User
    form_class = UserCreationForm
    template_name = 'user/user_create.html'
    success_url = reverse_lazy('user:user_created')

    def user_created(request, *args, **kwargs):
        
        if request.method == 'POST':
            form = UserCreationForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect(reverse('user:user_created'))
        
        else:
            form = UserCreationForm()

        return render(request, 'user/thanks_for_creating_user.html', context={'form': form})


class UserLoginView(LoginView):
    """Login page."""
    template_name = 'user/login.html'
    success_url = 'https://www.nrk.no/'
