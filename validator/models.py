from django.db import models

import uuid

class APIKey(models.Model):
    key = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    usage_count = models.PositiveIntegerField(default=0)
    rate_limit = models.PositiveIntegerField(default=100) #per hour

    def __str__(self):
        return str(self.key)

class NationalID(models.Model):
    nid = models.CharField(max_length=14, unique=True)
    birth_date = models.DateField()
    governorate_code = models.CharField(max_length=2)
    gender = models.CharField(max_length=6)

    validated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nid
