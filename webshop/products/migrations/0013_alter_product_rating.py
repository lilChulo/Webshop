# Generated by Django 5.0.6 on 2024-07-11 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_productpdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
