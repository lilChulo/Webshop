# Generated by Django 5.0.6 on 2024-06-26 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_product_rating_cart_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
