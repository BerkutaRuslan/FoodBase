# Generated by Django 3.0.6 on 2020-10-26 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'verbose_name_plural': 'Employee'},
        ),
        migrations.AlterModelOptions(
            name='resetkey',
            options={'verbose_name_plural': 'Reset key'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name_plural': 'Users'},
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(default='users/default.png', upload_to='users'),
        ),
    ]