from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class AmateurUser(AbstractUser):
    class Meta:
        db_table = 'amateuruser'

    user_id = models.AutoField(
        primary_key=True,
        unique=True,
    )
    username = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            RegexValidator('^[a-zA-Z0-9]*$',
                           message='半角英数字を使用してください'
                           ),
        ]
    )
    email = models.EmailField(
        unique=True,
        blank=True,
    )
    password = models.CharField(
        max_length=255,
    )
    is_active = models.BooleanField(
        default=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.username
