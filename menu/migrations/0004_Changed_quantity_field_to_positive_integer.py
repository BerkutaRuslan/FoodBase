# Generated by Django 3.0.6 on 2020-12-17 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_cart_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
