# Generated by Django 4.2.14 on 2024-07-14 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_reportedreview'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reportedreview',
            options={'verbose_name': 'Reported Review', 'verbose_name_plural': 'Reported Reviews'},
        ),
        migrations.AlterUniqueTogether(
            name='reportedreview',
            unique_together=set(),
        ),
    ]
