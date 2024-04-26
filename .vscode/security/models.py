from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from .manager import UserManager

Image_extension_validator = FileExtensionValidator(
    allowed_extensions=['jpg', 'jpeg', 'png', 'gif'],
    message='Upload an image file (JPG, JPEG, PNG, GIF) only.'
)

GENDER_CHOICE = (
    ('p_n_t_s', 'Prefer not to say'),
    ('m', 'Male'),
    ('f', 'Female'),
    ('o', 'Others')
)


def picture_path(instance, filename):
    return f'{instance}/{filename}'


class User(AbstractBaseUser):
    phone = models.CharField(
        _("phone number"), max_length=15,
        null=True, blank=True
    )
    picture = models.ImageField(
        _('profile picture'),
        upload_to=picture_path,
        blank=True,
        validators=[Image_extension_validator]
    )
    first_name = models.CharField(
        _("first name"),
        null=True, blank=True,
        max_length=50
    )
    last_name = models.CharField(
        _("last name"),
        null=True, blank=True,
        max_length=50
    )
    gender = models.CharField(
        _("gender"),
        choices=GENDER_CHOICE,
        default='p_n_t_s',
        null=True, blank=True,
        max_length=15
    )
    pincode = models.CharField(
        _("pincode"), max_length=6,
        null=True, blank=True,
    )
    email = models.EmailField(
        _("email address"), unique=True,
        primary_key=True,
    )
    is_active = models.BooleanField(
        _("active status"), default=True
    )
    is_superuser = models.BooleanField(
        _("superuser status"), default=False
    )
    is_staff = models.BooleanField(
        _("staff status"), default=False
    )
    is_agent = models.BooleanField(
        _("agent status"), default=False
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        return f"{self.email}"

    @staticmethod
    def has_perm(perm, obj=None, **kwargs):
        return True

    @staticmethod
    def has_module_perms(app_label, **kwargs):
        return True
