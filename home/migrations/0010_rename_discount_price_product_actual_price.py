# Generated by Django 5.1.1 on 2024-11-22 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_remove_cartitem_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='discount_price',
            new_name='actual_price',
        ),
    ]
