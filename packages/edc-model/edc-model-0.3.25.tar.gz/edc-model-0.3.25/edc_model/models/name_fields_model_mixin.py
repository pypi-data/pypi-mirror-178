from django.core.validators import RegexValidator
from django.db import models
from django_crypto_fields.fields import EncryptedCharField


class NameFieldsModelMixin(models.Model):
    legal_name = EncryptedCharField(
        verbose_name="Full name",
        blank=False,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^(([A-Z]+ )*[A-Z]+)?$",
                message=(
                    "Ensure full name consists of letters only in upper case "
                    "separated by single spaces"
                ),
            )
        ],
    )

    familiar_name = EncryptedCharField(
        verbose_name="How should we refer to you? (if we speak to you)",
        blank=False,
        validators=[
            RegexValidator(
                regex=r"^(([A-Z]+ )*[A-Z]+)?$",
                message=(
                    "Ensure name consists of letters only in upper case "
                    "separated by single spaces"
                ),
            )
        ],
    )

    class Meta:
        abstract = True
