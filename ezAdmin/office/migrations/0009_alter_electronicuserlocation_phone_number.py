# Generated by Django 4.2.4 on 2023-11-29 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0008_alter_electronicpurchasingdocument_invoice_doc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electronicuserlocation',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
