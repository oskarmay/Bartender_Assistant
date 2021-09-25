# Generated by Django 3.2.7 on 2021-09-25 18:07

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20210925_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientneeded',
            name='amount',
            field=models.DecimalField(decimal_places=3, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0'))], verbose_name='amount needed'),
        ),
        migrations.AlterField(
            model_name='ingredientstorage',
            name='storage_amount',
            field=models.DecimalField(decimal_places=3, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0'))], verbose_name='amount in storage'),
        ),
    ]
