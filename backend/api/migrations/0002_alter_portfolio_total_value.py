# Generated by Django 4.2 on 2025-02-20 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='total_value',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
    ]
