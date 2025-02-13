from uuid import uuid4

from django.conf import settings
from django.db import models


class Token(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_token',
    )
    key = models.UUIDField(unique=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.key)
