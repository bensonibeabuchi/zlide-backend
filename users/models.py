from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True, max_length=255, error_messages={"unique": _("A user with this email already exists."),},)
    first_name = models.CharField(_("first name"), max_length=255)
    last_name = models.CharField(_("last name"), max_length=255)
    job_title = models.CharField(_("job title"), max_length=255, default="No Job specified", blank=True, null=True)
    company = models.CharField(_("company name"), max_length=255, default="No company specified", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    otp = models.CharField(max_length=6, blank=True, null=True) 


    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'job_title', 'company']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        if not self.job_title:
            self.job_title = "No Job specified"
        if not self.company:
            self.company = "No company specified"
        super().save(*args, **kwargs)