from django.db import models
from django.contrib.auth.models import User
import os


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=100, decimal_places=2)
    product_info_pdf = models.FileField(upload_to='product_pdfs/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    other_field = models.CharField(max_length=255, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)

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


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')
        
    def vote(self, user, up_or_down):
        possible_votes = {
            'up': 'U',
            'down': 'D'
        }
        users_vote = possible_votes.get(up_or_down)
        
        # Check if the user has already voted for this review
        existing_vote = self.vote_set.filter(user=user).first()
        
        # If there is an existing vote, remove it
        if existing_vote:
            existing_vote.delete()

        if users_vote is not None:
            vote = Vote.objects.create(
                up_or_down=users_vote,
                user=user,
                review=self
            )
        else:
            print('Invalid Vote value!! : ', up_or_down)
    
    def get_upvotes(self):
        upvotes = Vote.objects.filter(up_or_down='U', review=self)
        return upvotes
    
    def get_upvotes_count(self):
        upvotes = self.get_upvotes()
        return len(upvotes)

    def get_downvotes(self):
        downvotes = Vote.objects.filter(up_or_down='D', review=self)
        return downvotes
    
    def get_downvotes_count(self):
        return len(self.get_downvotes())

    def __str__(self):
        return f'Review for {self.product.name} by {self.user.username}'
    
class Vote(models.Model):
    VOTE_TYPES = [
        ('U', 'up'),
        ('D', 'down'),
    ]
    up_or_down = models.CharField(max_length=1, choices=VOTE_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.up_or_down} on {self.review} by {self.user.username}'

    def __repr__(self):
        return f'{self.up_or_down} on {self.review} by {self.user.username} ({self.timestamp})'


class ProductPDF(models.Model):
    product = models.ForeignKey(Product, related_name='pdfs', on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='product_pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} PDF"
