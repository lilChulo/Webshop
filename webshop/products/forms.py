from django import forms
from django.forms import inlineformset_factory
from .models import Product, ProductImage, Review

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
    reason = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    def clean(self):
        cleaned_data = super().clean()
        reason = cleaned_data.get('reason')

        return cleaned_data


class ReportForm(forms.Form):
    reason = forms.CharField(max_length=200, help_text='Enter the reason for reporting this review')
