"""
Accounts Models - KaamSetu
Phone-based auth. No email. No password. OTP only.
"""
import random
import string
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, phone, role='worker', **extra_fields):
        if not phone:
            raise ValueError('Phone number is required')
        user = self.model(phone=phone, role=role, **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.model(phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_WORKER = 'worker'
    ROLE_CONTRACTOR = 'contractor'
    ROLE_CHOICES = [
        ('worker', 'Worker'),
        ('contractor', 'Contractor'),
    ]
    phone = models.CharField(max_length=15, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='worker')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'accounts_user'

    def __str__(self):
        return f"{self.name} ({self.phone}) [{self.role}]"

    @property
    def is_worker(self):
        return self.role == 'worker'

    @property
    def is_contractor(self):
        return self.role == 'contractor'


class OTP(models.Model):
    phone = models.CharField(max_length=15, db_index=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    attempts = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'accounts_otp'
        ordering = ['-created_at']

    def __str__(self):
        return f"OTP:{self.phone}"

    @property
    def is_expired(self):
        expiry = self.created_at + timezone.timedelta(minutes=getattr(settings, 'OTP_EXPIRY_MINUTES', 10))
        return timezone.now() > expiry

    @property
    def is_valid(self):
        return not self.is_used and not self.is_expired and self.attempts < 3

    @classmethod
    def generate(cls, phone):
        cls.objects.filter(phone=phone, is_used=False).update(is_used=True)
        code = ''.join(random.choices(string.digits, k=6))
        return cls.objects.create(phone=phone, code=code)
