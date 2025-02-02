from django import forms
from django.forms import inlineformset_factory
from .models import Product, ProductImage, Review, ReportedReview

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'product_info_pdf']

class ProductImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')  
    class Meta:
        model = ProductImage
        fields = ['images']

ProductImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=3, max_num=7, validate_max=True)
# https://docs.djangoproject.com/en/5.0/ref/forms/models/

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

class ReportReviewForm(forms.Form):
    reason = forms.CharField(max_length=100, required=True)