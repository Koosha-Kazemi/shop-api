# Generated by Django 5.1.7 on 2025-03-27 08:48

import django.db.models.deletion
import product.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_productattribute'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=product.models.product_image_path, verbose_name='Image file')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last updated')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('index', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_relations', to='product.image', verbose_name='Image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='product.product', verbose_name='Related Product')),
            ],
            options={
                'verbose_name': 'Product Image',
                'verbose_name_plural': 'Product Images',
                'ordering': ('image__index',),
                'unique_together': {('product', 'image')},
            },
        ),
    ]
