# Generated by Django 4.2 on 2024-06-18 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_productimage_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='image',
        ),
        migrations.AddField(
            model_name='productimage',
            name='images',
            field=models.FileField(blank=True, null=True, upload_to='product_image_upload_to'),
        ),
    ]
