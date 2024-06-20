from django.db import models
from django.contrib.auth.models import User
import os

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_info_pdf = models.FileField(upload_to='product_pdfs/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def product_image_upload_to(instance, filename):
    return os.path.join('product_pictures', str(instance.product.id), filename)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    # image = models.ImageField(upload_to=product_image_upload_to)
    images = models.FileField(upload_to=product_image_upload_to, null=True, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"
