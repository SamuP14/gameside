# Generated by Django 5.1.5 on 2025-01-27 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('slug', models.SlugField(max_length=268, unique=True)),
                ('description', models.TextField(blank=True)),
                ('logo', models.ImageField(default='logos/nologo.png', upload_to='logos')),
            ],
        ),
    ]
