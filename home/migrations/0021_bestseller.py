# Generated by Django 5.1.1 on 2024-11-23 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_homepagebanner_tagline_alter_homepagebanner_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='BestSeller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ManyToManyField(to='home.product')),
            ],
        ),
    ]
