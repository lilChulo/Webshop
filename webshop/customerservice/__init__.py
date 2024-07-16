from django.apps import AppConfig

class CustomerServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'

    def ready(self):
        import products.templatetags 