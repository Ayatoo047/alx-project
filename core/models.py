from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.contrib.auth.models import User

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)

class Domain(DomainMixin):
    pass


class TenantProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name='tenant_profile')
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    # profile_image = models.ImageField(upload_to='profile_images', null=True, blank=True, default='profile_images/user-default.png')
    bio = models.TextField(null=True, blank=True)
    tenant = models.CharField(max_length=500, null=True, blank=True)