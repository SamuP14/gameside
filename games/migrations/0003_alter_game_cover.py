# Generated by Django 5.1.5 on 2025-01-28 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_alter_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='cover',
            field=models.ImageField(default='covers/default.jpg', upload_to='covers'),
        ),
    ]
