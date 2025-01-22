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
        related_name='category_games',
        on_delete=models.SET_NULL,
    )
    platforms = models.ManyToManyField('platforms.Platform', related_name='platforms_games')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
