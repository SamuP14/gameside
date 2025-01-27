from uuid import uuid4

from django.conf import settings
from django.db import models


class Order(models.Model):
    class Status(models.IntegerChoices):
        CANCELLED = -1
        INITIATED = 1
        CONFIRMED = 2
        PAID = 3

    status = models.SmallIntegerField(choices=Status, default=Status.INITIATED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    key = models.UUIDField(blank=True, default=uuid4)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_orders',
        on_delete=models.CASCADE,
    )
    games = models.ManyToManyField('games.Game', related_name='game_orders')

    def __str__(self):
        return f'{self.status}'
