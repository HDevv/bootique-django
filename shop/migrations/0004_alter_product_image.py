# Generated by Django 5.2.4 on 2025-07-23 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_remove_product_disponible_product_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
