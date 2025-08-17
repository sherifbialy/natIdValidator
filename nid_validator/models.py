from django.db import models
from django.utils import timezone
import hashlib
import time


import uuid

class APIKey(models.Model):
    key = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    email = models.CharField(max_length=100, blank=True, null=True)
    monthly_quota = models.PositiveIntegerField(default=1000)
    usage_count = models.PositiveIntegerField(default=0)
    last_reset = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_key(email):
        raw = f"{email}-{time.time()}"
        unhashed = hashlib.sha256(raw.encode()).hexdigest()
        return unhashed

    @classmethod
    def create_with_email(cls, email, name=None, monthly_quota=10):
        
        unhashed = cls.generate_key(email)
        hashed = hashlib.sha256(unhashed.encode()).hexdigest()
        instance = cls.objects.create(
            key=hashed,
            email=email,
            monthly_quota=monthly_quota
        )
        return instance, unhashed

    def check_key(self, unhashed_key):
        return self.key == hashlib.sha256(unhashed_key.encode()).hexdigest()

    def increment_usage(self):
        self.refresh_quota_if_needed()
        if self.usage_count >= self.monthly_quota:
            return False
        self.usage_count += 1
        self.save()
        return True

    def refresh_quota_if_needed(self):
        now = timezone.now()
        if (self.last_reset.year, self.last_reset.month) != (now.year, now.month):
            self.usage_count = 0
            self.last_reset = now
            self.save()

    def __str__(self):
        return f"{self.email or 'Unnamed'} ({self.key})"



class NationalID(models.Model):
    nid = models.CharField(max_length=14, unique=True)
    birth_date = models.DateField()
    governorate_code = models.CharField(max_length=2)
    gender = models.CharField(max_length=6)

    validated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nid
