from django.contrib import admin
from .models import Product, ProductImage, ProductPDF

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductPDFInline(admin.TabularInline):
    model = ProductPDF
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductPDFInline]
    list_display = ('name', 'price', 'created_at')
    search_fields = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Customer Service').exists():
            return qs
        return qs.none()

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='Customer Service').exists():
            return True
        return super().has_change_permission(request, obj)


admin.site.register(Product, ProductAdmin)
