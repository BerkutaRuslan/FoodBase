# Generated by Django 3.0.6 on 2020-10-26 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20201015_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='photo',
            field=models.ImageField(default='news/default.png', upload_to='news'),
        ),
    ]