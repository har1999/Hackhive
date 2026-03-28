"""
Auth Views — OTP-based login. No passwords. No email.
Phone → OTP → JWT tokens → done.
"""
import logging
from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import OTP
from .serializers import OTPRequestSerializer, OTPVerifySerializer, UserSerializer
from notifications.sms import send_otp_sms

logger = logging.getLogger(__name__)
User = get_user_model()


# ─── API VIEWS ────────────────────────────────────────────────────────────────

class RequestOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data['phone']
        name = serializer.validated_data.get('name', '')
        role = serializer.validated_data.get('role', 'worker')

        otp = OTP.generate(phone)
        send_otp_sms(phone, otp.code)

        # Create user if first time
        user, created = User.objects.get_or_create(
            phone=phone,
            defaults={'name': name, 'role': role}
        )
        if created:
            if role == 'worker':
                from workers.models import WorkerProfile
                WorkerProfile.objects.get_or_create(user=user)
            else:
                from contractors.models import ContractorProfile
                ContractorProfile.objects.get_or_create(user=user)

        return Response({
            'message': f'OTP sent to {phone}',
            'debug_otp': otp.code if __import__('django.conf', fromlist=['settings']).settings.DEBUG else None
        }, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']

        try:
            otp_obj = OTP.objects.filter(phone=phone, is_used=False).latest('created_at')
        except OTP.DoesNotExist:
            return Response({'error': 'No OTP found. Request a new one.'}, status=status.HTTP_400_BAD_REQUEST)

        otp_obj.attempts += 1
        otp_obj.save()

        if not otp_obj.is_valid:
            return Response({'error': 'OTP expired or too many attempts.'}, status=status.HTTP_400_BAD_REQUEST)

        if otp_obj.code != code:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        otp_obj.is_used = True
        otp_obj.save()

        user = User.objects.get(phone=phone)
        user.is_verified = True
        user.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)


# ─── TEMPLATE VIEWS ───────────────────────────────────────────────────────────

class LoginPageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/' if request.user.is_contractor else '/worker/feed/')
        return render(request, 'auth/login.html')

    def post(self, request):
        phone = request.POST.get('phone', '').strip()
        otp_code = request.POST.get('otp', '').strip()
        name = request.POST.get('name', '').strip()
        role = request.POST.get('role', 'worker')

        if not otp_code:
            # Step 1: Request OTP
            if not phone:
                messages.error(request, 'Phone number required')
                return render(request, 'auth/login.html')
            otp = OTP.generate(phone)
            send_otp_sms(phone, otp.code)
            user, created = User.objects.get_or_create(
                phone=phone, defaults={'name': name, 'role': role}
            )
            if created:
                if role == 'worker':
                    from workers.models import WorkerProfile
                    WorkerProfile.objects.get_or_create(user=user)
                else:
                    from contractors.models import ContractorProfile
                    ContractorProfile.objects.get_or_create(user=user)
            return render(request, 'auth/login.html', {'otp_sent': True, 'phone': phone, 'debug_otp': otp.code})
        else:
            # Step 2: Verify OTP
            try:
                otp_obj = OTP.objects.filter(phone=phone, is_used=False).latest('created_at')
                otp_obj.attempts += 1
                otp_obj.save()
                if otp_obj.is_valid and otp_obj.code == otp_code:
                    otp_obj.is_used = True
                    otp_obj.save()
                    user = User.objects.get(phone=phone)
                    user.is_verified = True
                    user.save()
                    login(request, user, backend='accounts.backends.PhoneAuthBackend')
                    if user.is_contractor:
                        return redirect('/contractor/dashboard/')
                    return redirect('/worker/feed/')
                else:
                    messages.error(request, 'Invalid or expired OTP')
                    return render(request, 'auth/login.html', {'otp_sent': True, 'phone': phone})
            except OTP.DoesNotExist:
                messages.error(request, 'No OTP found')
                return render(request, 'auth/login.html')


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('/auth/login/')
