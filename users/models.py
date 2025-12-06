from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserAccountManager(BaseUserManager):

    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("email must provided")
        email = self.normalize_email(email)

        user = self.model(email=email, name=name, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_realtor(self, email, name, password=None, **extra_fields):
        extra_fields["is_realtor"] = True
        return self.create_user(email, name, password, **extra_fields)

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, name, password, **extra_fields)


class UserAccount(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_realtor = models.BooleanField(default=False)

    # Google OAuth fields
    google_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    picture = models.URLField(max_length=500, null=True, blank=True)
    auth_provider = models.CharField(
        max_length=50,
        choices=[
            ("email", "Email"),
            ("google", "Google"),
        ],
        default="email",
    )

    REQUIRED_FIELDS = ["name"]
    USERNAME_FIELD = "email"

    objects = UserAccountManager()

    def __str__(self):
        return self.email
