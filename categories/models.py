from colorfield.fields import ColorField
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(unique=True, max_length=128)
    slug = models.SlugField(max_length=268, unique=True)
    description = models.TextField(blank=True)
    color = ColorField(blank=True, default='#ffffff')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
