from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import UserRegisterForm
from .serializers import UserCreateSerializer

User = get_user_model()


def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)

            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}')
                return redirect('login')
            else:
                return render(request, 'users/register.html', {'form': form})
        else:
            form = form = UserRegisterForm()
        context = {
            'form': form
        }
        return render(request, 'users/register.html', context)
    else:
        return redirect('music:index')


class UserLogin(auth_views.LoginView):
    template_name = 'users/login.html'


class UserLogout(auth_views.LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You have successfully logged out.")
        return super().dispatch(request, *args, **kwargs)


class RegisterView(APIView):
    # this allows users to register without being authenticated
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = UserCreateSerializer(data=data)

        try:
            username = data['username']
            first_name = data['first_name']
            last_name = data['last_name']
            password = data['password']

        except KeyError:
            return Response({
                'code': 'data_not_complete',
                'detail': 'All required field must be filled'
            })
        # checks the password by django validation standards
        try:
            validate_password(password)
        except ValidationError as e:
            return Response(
                {
                    'code': 'weak_password',
                    'detail': ''.join(list(e))
                }, status=status.HTTP_400_BAD_REQUEST
            )

        # checks if user has a unique username
        if User.objects.filter(username=username).exists():
            return Response(
                {
                    'code': 'username_exists',
                    'detail': 'this username is already in use'
                }, status=status.HTTP_400_BAD_REQUEST)

        elif serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'code': 'user_registered', 'detail': 'you have been registered successfully.'
                                                                  'you may now login'}, status=status.HTTP_201_CREATED)
