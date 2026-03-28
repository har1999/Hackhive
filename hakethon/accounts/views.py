"""
Auth Views — Password-based login & signup.
"""
import logging
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, UserSerializer

logger = logging.getLogger(__name__)
User = get_user_model()


# ─── API VIEWS ────────────────────────────────────────────────────────────────

class DirectLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data['phone']
        name = serializer.validated_data.get('name', '')
        role = serializer.validated_data.get('role', 'worker')

        user, created = User.objects.get_or_create_with_profile(phone=phone, name=name, role=role)
        user.is_verified = True
        user.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)


# ─── TEMPLATE VIEWS ───────────────────────────────────────────────────────────

class SignupPageView(View):
    def get(self, request):
        return render(request, 'auth/signup.html', {'skills': User.SKILL_CHOICES})

    def post(self, request):
        data = request.POST
        try:
            user = User.objects.create_user(
                phone=data.get('phone'),
                password=data.get('password'),
                name=data.get('name'),
                role=data.get('role'),
                primary_skill=data.get('primary_skill'),
                location_name=data.get('location_name'),
                latitude=float(data.get('latitude', 0)),
                longitude=float(data.get('longitude', 0))
            )
            login(request, user)
            return redirect('worker_feed' if user.is_worker else 'contractor_dashboard')
        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return render(request, 'auth/signup.html', {'skills': User.SKILL_CHOICES})

class LoginPageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('contractor_dashboard') if request.user.is_contractor else reverse('worker_feed'))
        return render(request, 'auth/login.html')

    def post(self, request):
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=phone, password=password)
        if user:
            login(request, user)
            return redirect(reverse('contractor_dashboard') if user.is_contractor else reverse('worker_feed'))
        
        messages.error(request, 'Invalid phone number or password')
        return render(request, 'auth/login.html')


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect(reverse('login'))
from django.shortcuts import render
from django.views import View

from django.shortcuts import render, redirect
from django.views import View

class SignupPageView(View):
    # 1. This handles loading the page normally
    def get(self, request):
        return render(request, 'auth/signup.html')

    # 2. ADD THIS: This handles the form submission
    def post(self, request):
        # Here is where you will eventually save the user to the database.
        # For example, getting the data from the form:
        # phone = request.POST.get('phone')
        # password = request.POST.get('password')
        
        print("Form submitted with data:", request.POST) # Prints to your terminal
        
        # After successfully signing up, redirect the user to the login page
        return redirect('login')