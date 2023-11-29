# Generated by Django 4.2.4 on 2023-11-29 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brandname',
            name='brand_name',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='brandname',
            name='company_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='item_code',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]