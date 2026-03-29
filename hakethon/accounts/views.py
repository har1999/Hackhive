"""
Auth Views — Password-based login & signup.
Clean final version (no errors)
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

logger = logging.getLogger(__name__)
User = get_user_model()


# ================= SIGNUP =================
class SignupPageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        return render(request, 'auth/signup.html', {
            'skills': User.SKILL_CHOICES,
            'form_data': {}
        })

    def post(self, request):
        data = request.POST

        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        password = data.get('password', '')
        confirm = data.get('confirm_password', '')
        role = data.get('role', 'worker')
        skill = data.get('primary_skill', '')
        location = data.get('location_name', '').strip()
        lat = data.get('latitude', '').strip()
        lng = data.get('longitude', '').strip()

        errors = []

        if not name:
            errors.append('Full name is required.')
        if not phone or len(phone) < 10:
            errors.append('Enter a valid phone number.')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters.')
        if password != confirm:
            errors.append('Passwords do not match.')
        if role == 'worker' and not skill:
            errors.append('Select a primary skill.')
        if User.objects.filter(phone=phone).exists():
            errors.append('Phone already registered.')

        if errors:
            for e in errors:
                messages.error(request, e)
            return render(request, 'auth/signup.html', {
                'skills': User.SKILL_CHOICES,
                'form_data': data
            })

        user = User.objects.create_user(
            phone=phone,
            password=password,
            name=name,
            role=role,
            primary_skill=skill if role == 'worker' else '',
            location_name=location,
            latitude=float(lat) if lat else None,
            longitude=float(lng) if lng else None,
        )

        if role == 'worker':
            from workers.models import WorkerProfile
            WorkerProfile.objects.get_or_create(user=user)
        else:
            from contractors.models import ContractorProfile
            ContractorProfile.objects.get_or_create(user=user)

        login(request, user)
        messages.success(request, f'Welcome {name}! 🎉')

        if user.is_contractor:
            return redirect('contractor_dashboard')
        return redirect('worker_feed')


# ================= LOGIN =================
class LoginPageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_contractor:
                return redirect('contractor_dashboard')
            return redirect('worker_feed')

        return render(request, 'auth/login.html')

    def post(self, request):
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')

        if not phone or not password:
            messages.error(request, 'Phone and password required.')
            return render(request, 'auth/login.html')

        user = authenticate(request, username=phone, password=password)

        if user:
            login(request, user)

            next_url = request.GET.get('next')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)

            if user.is_contractor:
                return redirect('contractor_dashboard')
            return redirect('worker_feed')

        messages.error(request, 'Invalid credentials.')
        return render(request, 'auth/login.html')


# ================= LOGOUT =================
class LogoutView(View):
    def post(self, request):  # ← fixed: POST not GET
        logout(request)
        return redirect('login')


# ================= DIRECT LOGIN (JWT) =================
class DirectLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({
            "error": "Invalid credentials"
        }, status=status.HTTP_401_UNAUTHORIZED)