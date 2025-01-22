from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class Game(models.Model):
    class PEGI(models.IntegerChoices):
        PEGI3 = 3
        PEGI7 = 7
        PEGI12 = 12
        PEGI16 = 16
        PEGI18 = 18

    title = models.CharField(max_length=218, unique=True)
    slug = models.SlugField(max_length=268, unique=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to='covers', default='covers/nocover.png')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.PositiveIntegerField()
    released_at = models.DateField()
    pegi = models.IntegerField(choices=PEGI)
    category = models.ForeignKey(
        'categories.Category',
        related_name='game_categories',
        on_delete=models.SET_NULL,
        null=True,
    )
    platforms = models.ManyToManyField('platforms.Platform', related_name='game_platforms')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Review(models.Model):
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    comment = models.TextField()
    game = models.ForeignKey('games.Game', related_name='game_reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='user_reviews', on_delete=models.CASCADE
    )
