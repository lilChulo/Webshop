# Generated by Django 5.0.6 on 2024-06-18 18:39

import products.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_remove_productimage_image_productimage_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='images',
            field=models.FileField(blank=True, null=True, upload_to=products.models.product_image_upload_to),
        ),
    ]
