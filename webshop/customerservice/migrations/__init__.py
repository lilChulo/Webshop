from django.db import migrations
from django.contrib.auth.models import Group

def create_customer_service_group(apps, schema_editor):
    Group.objects.get_or_create(name='CustomerService')

class Migration(migrations.Migration):

    dependencies = [
        # Ihre Abhängigkeiten hier
    ]

    operations = [
        migrations.RunPython(create_customer_service_group),
    ]
