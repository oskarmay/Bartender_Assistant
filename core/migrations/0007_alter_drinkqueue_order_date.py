# Generated by Django 3.2.7 on 2022-01-11 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_drinkqueue_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drinkqueue',
            name='order_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='order date'),
        ),
    ]