# Generated by Django 3.2.7 on 2021-12-08 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20211208_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientstorage',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='ingredients', verbose_name='image'),
        ),
    ]
