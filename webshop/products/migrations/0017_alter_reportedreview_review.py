# Generated by Django 4.2 on 2024-07-16 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_reportedreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportedreview',
            name='review',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports', to='products.review'),
        ),
    ]
