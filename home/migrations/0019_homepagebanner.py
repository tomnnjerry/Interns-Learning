# Generated by Django 5.1.1 on 2024-11-23 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_collection_display_in_home'),
    ]

    operations = [
        migrations.CreateModel(
            name='Homepagebanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('link', models.CharField(blank=True, max_length=255, null=True)),
                ('featured_image', models.ImageField(upload_to='homepage/')),
            ],
        ),
    ]
