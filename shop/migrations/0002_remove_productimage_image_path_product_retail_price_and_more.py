# Generated by Django 5.2 on 2025-04-18 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='image_path',
        ),
        migrations.AddField(
            model_name='product',
            name='retail_price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10, verbose_name='Цена розница'),
        ),
        migrations.AddField(
            model_name='product',
            name='wholesale_price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10, verbose_name='Цена оптом'),
        ),
        migrations.AddField(
            model_name='productimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/'),
        ),
    ]
