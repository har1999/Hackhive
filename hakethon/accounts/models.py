"""
Accounts Models - KaamSetu
Password-based auth with Geolocation and Skills.
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, role='worker', **extra_fields):
        if not phone:
            raise ValueError('Phone number is required')
        user = self.model(phone=phone, role=role, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def get_or_create_with_profile(self, phone, name='', role='worker'):
        user, created = self.get_or_create(phone=phone, defaults={'name': name, 'role': role})
        if created:
            if role == 'worker':
                from workers.models import WorkerProfile
                WorkerProfile.objects.get_or_create(user=user)
            else:
                from contractors.models import ContractorProfile
                ContractorProfile.objects.get_or_create(user=user)
        return user, created

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_WORKER = 'worker'
    ROLE_CONTRACTOR = 'contractor'
    ROLE_CHOICES = [
        ('worker', 'Worker'),
        ('contractor', 'Contractor'),
    ]
    SKILL_CHOICES = [
        ('mason', 'Mason'),
        ('electrician', 'Electrician'),
        ('painter', 'Painter'),
        ('labourer', 'Labourer'),
    ]

    phone = models.CharField(max_length=15, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='worker')
    
    # Profile Fields
    primary_skill = models.CharField(max_length=30, choices=SKILL_CHOICES, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    location_name = models.CharField(max_length=200, blank=True)

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
