import hashid_field

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group
)
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model(
            email=self.normalize_email(email).lower(),
            **extra_fields
        )
        user.set_password(password)
        user_group, _ = Group.objects.get_or_create(name="user")
        user.save(using=self._db)
        user.groups.add(user_group)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(
            email,
            password=password,
            **extra_fields
        )
        admin_group, _ = Group.objects.get_or_create(name="admin")
        user.is_superuser = True
        user.groups.add(admin_group)
        user.save(using=self._db)
        return user

    def filter_admins(self):
        return self.filter(groups__name="admin")


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model representing user in the system."""
    id = hashid_field.HashidAutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        """Return string representation of the object."""
        return str(self.email)

    def has_perm(self, perm, obj=None):
        """Check if the user have a specific permission."""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Check if the user have permissions to view the app `app_label."""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Check if the user a member of staff."""
        # Simplest possible answer: All admins are staff
        return self.is_admin